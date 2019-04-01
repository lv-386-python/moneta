from inspect import isfunction
import nose
import unittest
import pool_manager


CONN = {'connection':'mocked connection',
        'last_update': 0,
        'create_time': 0.0}

class MySQLdbMock:
    '''mocked mysql'''
    def __init__(self):
        '''init for mocked mysql'''
        self.txt = 'mocked connection'


class ConnectionMock(MySQLdbMock):
    '''mocked connection'''

    def connect(self, **kwargs):
        '''mocked funcion connect'''
        return ConnectionMock()

    def close(self):
        '''mocked funcion close'''

    def roolback(self):
        '''mocked funcion roolback'''

    def commit(self):
        '''mocked funcion commit'''

    def cursor(self):
        '''mocked funcion cursor'''
        return None


class DBPoolManagerTest(unittest.TestCase):
    """docstring for DBPoolManagerTest"""

    def setUp(self):
        '''setup function'''
        self.true_MySQLdb = pool_manager.MySQLdb
        pool_manager.MySQLdb = ConnectionMock()

    def tearDown(self):
        '''tearDown function'''
        pool_manager.MySQLdb = self.true_MySQLdb

    def test_create_connection(self):
        '''test for creating new connection'''
        case_1 = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)._create_connection()
        nose.tools.eq_(case_1['connection'].txt, 
                       'mocked connection',
                       msg=None)

    def test_get_connection_new(self):
        '''test for getting new connection'''
        pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        pool._get_connection()
        nose.tools.eq_(pool._connection_counter,
                       1,
                       msg=None)

    def test_get_connection_old(self):
        '''test for getting connection from pool'''
        pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        pool._pool = [CONN]
        nose.tools.eq_(pool._get_connection(),
                       CONN,
                       msg=None)

    def test_return_connection(self):
        '''test for return connection'''
        pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        conn = pool._get_connection()
        nose.tools.eq_(len(pool._pool),
                       0,
                       msg=None)
        pool._return_connection(conn)
        nose.tools.eq_(len(pool._pool),
                       1,
                       msg=None)

    def test_close_connection(self):
        '''test for closing connection'''
        pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        conn = pool._get_connection()
        nose.tools.eq_(pool._connection_counter,
                       1,
                       msg=None)
        pool._close_connection(conn)
        nose.tools.eq_(pool._connection_counter,
                       0,
                       msg=None)

    def test_repeat_decorator(self):
        '''test for decorator'''

        @pool_manager.re_request()
        def function():
            '''function for test'''
            return True

        nose.tools.eq_(function(),
                       True,
                       msg=None)

    def test_repeat_decorator_error(self):
        '''test if decorator raise error'''

        @pool_manager.re_request()
        def function():
            '''function for test'''
            raise pool_manager.DBManagerError

        nose.tools.assert_raises(pool_manager.DBManagerError,
                                 function(),
                                 msg=None)

    def test_return_pool_manager_new(self):
        '''test for creating new pool_manager'''
        nose.tools.assert_is_instance(pool_manager.pool_manage(),
                                      pool_manager.DBPoolManager,
                                      msg=None)


    def test_return_pool_manager_exist(self):
        '''test for singleton pool_manager'''
        pool1 = pool_manager.pool_manage()
        pool2 = pool_manager.pool_manage()
        nose.tools.assert_is(pool1,
                             pool2,
                             msg=None)

    def test_manage(self):
        '''test for manage'''
        pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        with pool.manage() as man:
            nose.tools.eq_(man.txt,
                           'mocked connection',
                           msg=None)
        nose.tools.eq_(pool._connection_counter,
                       0,
                       msg=None)
            
    def test_manage_error(self):
        '''test if manage raise error'''
        pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        with pool.manage() as man:
            raise pool_manager.DBManagerError
        nose.tools.assert_raises(pool_manager.DBManagerError,
                                 msg=None)
        nose.tools.eq_(pool._connection_counter,
                         0,
                         msg=None)

    def test_transaction(self):
        '''test for transactions'''
        pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        with pool.transaction() as man:
            nose.tools.eq_(pool._connection_counter,
                           1,
                           msg=None)
        nose.tools.eq_(pool._connection_counter,
                       0,
                       msg=None)


if __name__ == '__main__':
    nose.main()
