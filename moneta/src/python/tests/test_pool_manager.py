import unittest
import nose

from src.python.helper import pool_manager

CONN = {'connection': 'mocked connection',
        'last_update': 0,
        'create_time': 0.0}

class MySQLdbMock:
    '''mocked mysql'''
    def __init__(self):
        '''init for mocked mysql'''
        self.txt = 'mocked connection'

s
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
    pool = None
    pool1 = None
    pool2 = None


    def setUp(self):
        '''setup function'''
        self.true_mysql = pool_manager.MySQLdb
        pool_manager.MySQLdb = ConnectionMock()

    def tearDown(self):
        '''tearDown function'''
        pool_manager.MySQLdb = self.true_mysql

    def test_create_connection(self):
        '''test for creating new connection'''
        self.pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)._create_connection()
        nose.tools.eq_(self.pool['connection'].txt, 
                       'mocked connection')

    def test_get_connection_new(self):
        '''test for getting new connection'''
        self.pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        self.pool._get_connection()
        nose.tools.eq_(self.pool._connection_counter,
                       1)

    def test_get_connection_old(self):
        '''test for getting connection from pool'''
        self.pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        self.pool._pool = [CONN]
        nose.tools.eq_(self.pool._get_connection(),
                       CONN)

    def test_return_connection(self):
        '''test for return connection'''
        self.pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        conn = self.pool._get_connection()
        nose.tools.eq_(len(self.pool._pool),
                       0)
        self.pool._return_connection(conn)
        nose.tools.eq_(len(self.pool._pool),
                       1)

    def test_close_connection(self):
        '''test for closing connection'''
        self.pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        conn = self.pool._get_connection()
        nose.tools.eq_(self.pool._connection_counter,
                       1)
        self.pool._close_connection(conn)
        nose.tools.eq_(self.pool._connection_counter,
                       0)

    def test_repeat_decorator(self):
        '''test for decorator'''

        @pool_manager.re_request()
        def function():
            '''function for test'''
            return True

        nose.tools.eq_(function(),
                       True)

    def test_repeat_decorator_error(self):
        '''test if decorator raise error'''

        @pool_manager.re_request()
        def function():
            '''function for test'''
            raise pool_manager.DBManagerError

        nose.tools.assert_raises(pool_manager.DBManagerError,
                                 function())

    def test_return_pool_manager_new(self):
        '''test for creating new pool_manager'''
        nose.tools.assert_is_instance(pool_manager.pool_manage(),
                                      pool_manager.DBPoolManager)


    def test_return_pool_manager_exist(self):
        '''test for singleton pool_manager'''
        self.pool1 = pool_manager.pool_manage()
        self.pool2 = pool_manager.pool_manage()
        nose.tools.assert_is(self.pool1,
                             self.pool2)

    def test_manage(self):
        '''test for manage'''
        self.pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        with self.pool.manage() as man:
            nose.tools.eq_(man.txt,
                           'mocked connection')
        nose.tools.eq_(self.pool._connection_counter,
                       0)
            
    def test_manage_error(self):
        '''test if manage raise error'''
        self.pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        with self.pool.manage() as man:
            raise pool_manager.DBManagerError
        nose.tools.assert_raises(pool_manager.DBManagerError)
        nose.tools.eq_(self.pool._connection_counter,
                       0)

    def test_transaction(self):
        '''test for transactions'''
        self.pool = pool_manager.DBPoolManager(**pool_manager.CONNECT_SETTINGS)
        with self.pool.transaction() as man:
            nose.tools.eq_(self.pool._connection_counter,
                           1)
        nose.tools.eq_(self.pool._connection_counter,
                       0)


if __name__ == '__main__':
    nose.main()
