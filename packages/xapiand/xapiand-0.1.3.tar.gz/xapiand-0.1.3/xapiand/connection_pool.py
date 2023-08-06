# Copyright (c) 2019 Dubalu LLC
# Copyright (c) 2017 Elasticsearch
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to you under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import time
import random
import logging
import threading

try:
    from Queue import PriorityQueue, Empty
except ImportError:
    from queue import PriorityQueue, Empty

from .utils import jump_consistent_hash
from .exceptions import ImproperlyConfigured

logger = logging.getLogger('xapiand')


class ConnectionSelector(object):
    """
    Simple class used to select a connection from a list of currently live
    connection instances. In init time it is passed a dictionary containing all
    the connections' options which it can then use during the selection
    process. When the `select` method is called it is given a list of
    *currently* live connections to choose from.

    The options dictionary is the one that has been passed to
    :class:`~xapiand.Transport` as `hosts` param and the same that is
    used to construct the Connection object itself. When the Connection was
    created from information retrieved from the cluster via the sniffing
    process it will be the dictionary returned by the `host_info_callback`.

    Example of where this would be useful is a zone-aware selector that would
    only select connections from it's own zones and only fall back to other
    connections where there would be none in it's zones.
    """
    def select(self, pool, **kwargs):
        """
        Select a connection from the given list.

        :arg pool: connection pool to choose connections from
        """
        pass


class RandomSelector(ConnectionSelector):
    """
    Select a connection at random
    """
    def select(self, pool, **kwargs):
        return random.choice(pool.connections)


class RoundRobinSelector(ConnectionSelector):
    """
    Selector using round-robin.
    """
    def __init__(self):
        super(RoundRobinSelector, self).__init__()
        self.data = threading.local()

    def select(self, pool, **kwargs):
        connections = pool.connections
        self.data.rr = getattr(self.data, 'rr', -1) + 1
        self.data.rr %= len(connections)
        return connections[self.data.rr]


class RoutingSelector(ConnectionSelector):
    """
    Select a connection from hashing url or routing param
    """
    def select(self, pool, **kwargs):
        routing = kwargs['params'].get('routing', kwargs['path'])
        connections = pool.orig_connections
        size = len(connections)
        idx = jump_consistent_hash(routing, size)
        for i in range(size):
            connection = connections[(idx + i) % size]
            if connection not in pool.dead_count:
                return connection


class ConnectionPool(object):
    """
    Container holding the :class:`~xapiand.Connection` instances,
    managing the selection process (via a
    :class:`~xapiand.ConnectionSelector`) and dead connections.

    It's only interactions are with the :class:`~xapiand.Transport` class
    that drives all the actions within `ConnectionPool`.

    Initially connections are stored on the class as a list and, along with the
    connection options, get passed to the `ConnectionSelector` instance for
    future reference.

    Upon each request the `Transport` will ask for a `Connection` via the
    `get_connection` method. If the connection fails (it's `perform_request`
    raises a `ConnectionError`) it will be marked as dead (via `mark_dead`) and
    put on a timeout (if it fails N times in a row the timeout is exponentially
    longer - the formula is `default_timeout * 2 ** (fail_count - 1)`). When
    the timeout is over the connection will be resurrected and returned to the
    live pool. A connection that has been previously marked as dead and
    succeeds will be marked as live (its fail count will be deleted).
    """
    def __init__(self, connections, dead_timeout=60, timeout_cutoff=5,
                 selector_class=RoutingSelector, **kwargs):
        """
        :arg connections: list of tuples containing the
            :class:`~xapiand.Connection` instance and it's options
        :arg dead_timeout: number of seconds a connection should be retired for
            after a failure, increases on consecutive failures
        :arg timeout_cutoff: number of consecutive failures after which the
            timeout doesn't increase
        :arg selector_class: :class:`~xapiand.ConnectionSelector`
            subclass to use if more than one connection is live
        """
        if not connections:
            raise ImproperlyConfigured(
                "No defined connections, you need to specify at least one host.")
        self.connection_opts = connections
        self.connections = [c for (c, opts) in connections]
        # remember original connection list for resurrect(force=True)
        self.orig_connections = tuple(self.connections)
        # PriorityQueue for thread safety and ease of timeout management
        self.dead = PriorityQueue(len(self.connections))
        self.dead_count = {}

        # default timeout after which to try resurrecting a connection
        self.dead_timeout = dead_timeout
        self.timeout_cutoff = timeout_cutoff

        self.selector = selector_class()
        for connection in self.orig_connections:
            if connection.active is False:
                self.mark_dead(connection)

    def mark_dead(self, connection, now=None):
        """
        Mark the connection as dead (failed). Remove it from the live pool and
        put it on a timeout.

        :arg connection: the failed instance
        """
        # allow inject for testing purposes
        now = now if now else time.time()
        try:
            self.connections.remove(connection)
        except ValueError:
            # connection not alive or another thread marked it already, ignore
            return
        else:
            dead_count = self.dead_count.get(connection, 0) + 1
            self.dead_count[connection] = dead_count
            timeout = self.dead_timeout * 2 ** min(dead_count - 1, self.timeout_cutoff)
            self.dead.put((now + timeout, connection))
            logger.warning(
                "Connection %r has failed for %i times in a row, putting on %i second timeout.",
                connection, dead_count, timeout
            )

    def mark_live(self, connection):
        """
        Mark connection as healthy after a resurrection. Resets the fail
        counter for the connection.

        :arg connection: the connection to redeem
        """
        try:
            del self.dead_count[connection]
        except KeyError:
            # race condition, safe to ignore
            pass

    def resurrect(self, force=False):
        """
        Attempt to resurrect a connection from the dead pool. It will try to
        locate one (not all) eligible (it's timeout is over) connection to
        return to the live pool. Any resurrected connection is also returned.

        :arg force: resurrect a connection even if there is none eligible (used
            when we have no live connections). If force is specified resurrect
            always returns a connection.

        """
        # no dead connections
        if self.dead.empty():
            # we are forced to return a connection, take one from the original
            # list. This is to avoid a race condition where get_connection can
            # see no live connections but when it calls resurrect self.dead is
            # also empty. We assume that other threat has resurrected all
            # available connections so we can safely return one at random.
            if force:
                return random.choice(self.orig_connections)
            return

        try:
            # retrieve a connection to check
            timeout, connection = self.dead.get(block=False)
        except Empty:
            # other thread has been faster and the queue is now empty. If we
            # are forced, return a connection at random again.
            if force:
                return random.choice(self.orig_connections)
            return

        if not force and timeout > time.time():
            # return it back if not eligible and not forced
            self.dead.put((timeout, connection))
            return

        # either we were forced or the connection is elligible to be retried
        self.connections.append(connection)
        logger.info("Resurrecting connection %r (force=%s).", connection, force)
        return connection

    def get_connection(self, **kwargs):
        """
        Return a connection from the pool using the `ConnectionSelector`
        instance.

        It tries to resurrect eligible connections, forces a resurrection when
        no connections are availible and passes the list of live connections to
        the selector instance to choose from.

        Returns a connection instance and it's current fail count.
        """
        self.resurrect()
        connections = self.connections[:]

        # no live nodes, resurrect one by force and return it
        if not connections:
            return self.resurrect(True)

        # only call selector if we have a selection
        if len(connections) > 1:
            return self.selector.select(self, **kwargs)

        # only one connection, no need for a selector
        return connections[0]

    def close(self):
        """
        Explicitly closes connections
        """
        for conn in self.orig_connections:
            conn.close()


class DummyConnectionPool(ConnectionPool):
    def __init__(self, connections, **kwargs):
        if len(connections) != 1:
            raise ImproperlyConfigured(
                "DummyConnectionPool needs exactly one connection defined.")
        # we need connection opts for sniffing logic
        self.connection_opts = connections
        self.connection = connections[0][0]
        self.connections = (self.connection, )

    def get_connection(self, **kwargs):
        return self.connection

    def close(self):
        """
        Explicitly closes connections
        """
        self.connection.close()

    def _noop(self, *args, **kwargs):
        pass
    mark_dead = mark_live = resurrect = _noop
