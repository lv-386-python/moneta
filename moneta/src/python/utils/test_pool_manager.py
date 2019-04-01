import nose
import unittest
import pool_manager
import time
from inspect import isfunction


CONN = {'connection':'mocked connection',
        'last_update': 0,
        'create_time': 2.0}

class MySQLdbMock:
    def __init__(self):
        self.txt = 'mocked connection'


class ConnectionMock(MySQLdbMock):

    def connect(self, user, password, db, host, port, charset, init_command):
        return ConnectionMock()

    def close(self):
        pass


class DBPoolManagerTest(unittest.TestCase):
    """docstring for DBPoolManagerTest"""

    def setUp(self):
        self.true_MySQLdb = pool_manager.MySQLdb
        pool_manager.MySQLdb = ConnectionMock()

    def tearDown(self):
        pool_manager.MySQLdb = self.true_MySQLdb

    def test_create_connection(self):
        case_1 = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)._create_connection()
        nose.tools.eq_(case_1['connection'].txt, 'mocked connection', msg=None)

    def test_get_connection_new(self):
        pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        pool._get_connection()
        nose.tools.eq_(pool._connection_counter, 1, msg=None)

    def test_get_connection_old(self):
        pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        pool._pool = [CONN]
        nose.tools.eq_(pool._get_connection(), CONN, msg=None)

    def test_return_connection(self):
        pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        conn = pool._get_connection()
        nose.tools.eq_(len(pool._pool), 0, msg=None)
        pool._return_connection(conn)
        nose.tools.eq_(len(pool._pool), 1, msg=None)

    def test_close_connection(self):
        pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        conn = pool._get_connection()
        nose.tools.eq_(pool._connection_counter, 1, msg=None)
        pool._close_connection(conn)
        nose.tools.eq_(pool._connection_counter, 0, msg=None)

    def test_repeat_decorator(self):

        @pool_manager.re_request()
        def function():
            return True

        nose.tools.eq_(function(), True, msg=None)

    def test_repeat_decorator_error(self):

        @pool_manager.re_request()
        def function():
            raise pool_manager.DBManagerError

        nose.tools.assert_raises(pool_manager.DBManagerError, function(), msg=None)
        
    def test_return_pool_manager_new(self):
        nose.tools.assert_is_instance( pool_manager.pool_manage(), pool_manager.DBPoolManager, msg=None)


    def test_return_pool_manager_exist(self):
        pool1 = pool_manager.pool_manage()
        pool2 = pool_manager.pool_manage()
        nose.tools.assert_is(pool1, pool2, msg=None)


if __name__ == '__main__':
    nose.main()