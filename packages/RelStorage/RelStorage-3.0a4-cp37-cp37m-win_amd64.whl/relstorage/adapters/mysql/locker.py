##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Locker implementations.
"""

from __future__ import absolute_import
from __future__ import print_function

from zope.interface import implementer

from ..interfaces import ILocker
from ..interfaces import UnableToAcquireCommitLockError
from ..interfaces import UnableToAcquirePackUndoLockError
from ..locker import AbstractLocker


class CommitLockQueryFailedError(UnableToAcquireCommitLockError):
    pass

@implementer(ILocker)
class MySQLLocker(AbstractLocker):
    """
    MySQL locks.

    Two types of locks are used. The ordinary commit lock is a
    standard InnoDB row-level lock; this brings the benefits of being
    lightweight and automatically being released if the transaction
    aborts or commits, plus instant deadlock detection. Prior to MySQL
    8.0, these don't support ``NOWAIT`` syntax, so we synthesize that by
    setting the session variable `innodb_lock_wait_timeout
    <https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_lock_wait_timeout>`_.

    Note that this lock cannot be against the ``object_state`` or
    ``current_object`` tables: arbitrary rows in those tables may have
    been locked by other transactions, and we risk deadlock.

    Also note that by default, a lock timeout will only rollback the
    current *statement*, not the whole session, as in most databases
    (this doesn't apply to ``NOWAIT`` in MySQL 8). Fortunately, a lock timeout
    only rolling back the single statement is exactly what we want to implement
    ``NOWAIT`` on earlier databases.

    The ``ensure_current`` argument is essentially ignored; the locks
    taken out by ``lock_current_objects`` take care of that.

    The second type of lock, an advisory lock, is used for pack locks.
    This lock uses the `GET_LOCK
    <https://dev.mysql.com/doc/refman/5.7/en/locking-functions.html#function_get-lock>`_
    and ``RELEASE_LOCK`` functions. These locks persist for the
    duration of a session, and *must* be explicitly released. They do
    *not* participate in deadlock detection.

    Prior to MySQL 5.7.5, it is not possible to hold more than one
    advisory lock in a single session. In the past we used advisory
    locks for the commit lock, and that meant we had to use multiple
    sessions (connections) to be able to hold both the commit lock and
    the pack lock. Fortunately, that limitation has been lifted: we no
    longer support older versions of MySQL, and we don't need multiple
    advisory locks anyway.
    """

    def __init__(self, options, driver, batcher_factory):
        super(MySQLLocker, self).__init__(options, driver, batcher_factory)
        # TODO: Back to needing a proper prepare registry.
        lock_stmt_raw = self._commit_lock_query
        lock_stmt_nowait_raw = self._commit_lock_nowait_query

        self._prepare_lock_stmt = 'PREPARE hold_commit_lock FROM "%s"' % (
            lock_stmt_raw)
        self._prepare_lock_stmt_nowait = 'PREPARE hold_commit_lock_nowait FROM "%s"' % (
            lock_stmt_nowait_raw)
        self._supports_row_lock_nowait = None

        self._commit_lock_query = 'EXECUTE hold_commit_lock'
        self._commit_lock_nowait_query = 'EXECUTE hold_commit_lock_nowait'

        # No good preparing this, mysql can't take parameters in EXECUTE,
        # they have to be user variables, which defeats most of the point
        # (Although in this case, because it's a static value, maybe not;
        # it could be set once and re-used.)
        self.set_timeout_stmt = 'SET SESSION innodb_lock_wait_timeout = %s'

    def on_store_opened(self, cursor, restart=False):
        super(MySQLLocker, self).on_store_opened(cursor, restart=restart)
        if restart:
            return

        # MySQL 8 and above support NOWAIT on row locks.
        # sys.version_major() is 5.7.9+, but we don't have execute
        # permissions on that function by default, so we do it the old fashioned
        # way with version()
        if self._supports_row_lock_nowait is None:
            # TODO: Move this to a supporting MySQLVersionDetector.
            cursor.execute('SELECT version()')
            ver = cursor.fetchone()[0]
            # PyMySQL on Win/Py3 returns this as a byte string; everywhere
            # else it's native.
            ver = self._metadata_to_native_str(ver)
            major = int(ver[0])
            __traceback_info__ = ver, major
            self._supports_row_lock_nowait = (major >= 8)

        cursor.execute(self._prepare_lock_stmt)
        if self._supports_row_lock_nowait:
            cursor.execute(self._prepare_lock_stmt_nowait)

    def _on_store_opened_set_row_lock_timeout(self, cursor, restart=False):
        if restart:
            return
        self._set_row_lock_timeout(cursor, self.commit_lock_timeout)

    def _set_row_lock_timeout(self, cursor, timeout):
        # Min value of timeout is 1
        timeout = timeout if timeout >= 1 else 1
        cursor.execute(self.set_timeout_stmt, (timeout,))
        # It's INCREDIBLY important to fetch a row after we execute the SET statement;
        # otherwise, the binary drivers that use libmysqlclient tend to crash,
        # usually with a 'malloc: freeing not allocated data' or 'malloc:
        # corrupted data, written after free?' or something like that.
        cursor.fetchone()

    def release_commit_lock(self, cursor):
        "Auto-released by transaction end."

    def _get_commit_lock_debug_info(self, cursor):
        cursor.execute('SELECT connection_id()')
        conn_id = str(cursor.fetchone()[0])

        try:
            # MySQL 8
            cursor.execute('SELECT * FROM performance_schema.data_wait_locks')
            return 'Connection: ' + conn_id + '\n' + self._rows_as_pretty_string(cursor)
        except self.driver.driver_module.Error:
            # MySQL 5, or no permissions
            cursor.execute('SELECT * from information_schema.innodb_locks')
            rows = self._rows_as_pretty_string(cursor)
            return 'Connection: ' + conn_id + '\n' + rows

    def hold_pack_lock(self, cursor):
        """Try to acquire the pack lock.

        Raise an exception if packing or undo is already in progress.
        """
        stmt = "SELECT GET_LOCK(CONCAT(DATABASE(), '.pack'), 0)"
        cursor.execute(stmt)
        res = cursor.fetchone()[0]
        if not res:
            raise UnableToAcquirePackUndoLockError('A pack or undo operation is in progress')

    def release_pack_lock(self, cursor):
        """Release the pack lock."""
        stmt = "SELECT RELEASE_LOCK(CONCAT(DATABASE(), '.pack'))"
        cursor.execute(stmt)
        row = cursor.fetchone() # stay in sync
        assert row
