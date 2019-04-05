'''Module with pool manager for creating some pool of connections'''
import time
import threading
import MySQLdb
from contextlib import contextmanager # pylint:disable = wrong-import-order
from MySQLdb.cursors import DictCursor
from src.python.core import utils
from src.python.core.constants import CREATE_TIME, CONNECTION, LAST_UPDATE
from src.python.core.decorators import singleton


class DBManagerError(Exception):
    '''Error of DB or pool manager.'''


@singleton
class DBPoolManager:
    '''Class for managing connections to the DB'''
    def __init__(self):
        '''creating new instance of DB _pool manager'''
        data = utils.get_config()
        self._connection_counter = 0
        self._pool = []
        self.lock = threading.RLock()
        self.database = data['moneta']['database']
        self.user = data['moneta']['user']
        self.port = data['moneta']['port']
        self.password = data['moneta']['password']
        self.lifetime = data['moneta']['lifetime']
        self.delay = data['moneta']['delay']
        self.poolsize = data['moneta']['poolsize']

    def __del__(self):
        '''method for deleting connection from memory'''
        for connect in self._pool:
            self._close_connection(connect)

    def _create_connection(self):
        '''create a new connection'''
        connection = MySQLdb.connect(database=self.database,
                                     user=self.user,
                                     password=self.password,
                                     port=self.port)
        self._connection_counter += 1
        return {CONNECTION: connection,
                LAST_UPDATE: 0,
                CREATE_TIME: time.time()}

    def _get_connection(self):
        '''get connection from the connection _pool'''
        connect = None
        while not connect:
            if self._pool:
                connect = self._pool.pop()
            elif self._connection_counter < self.poolsize:
                connect = self._create_connection()
            time.sleep(self.delay)
        return connect

    def _close_connection(self, connection):
        '''close old and uselese connection'''
        connection[CONNECTION].close()
        self._connection_counter -= 1

    def _return_connection(self, connection):
        '''return connection to the _pool'''
        connection[LAST_UPDATE] = time.time()
        self._pool.append(connection)

    @contextmanager
    def get_connect(self):
        '''Context manager for getting connection.'''
        with self.lock:
            connection = self._get_connection()
        try:
            yield connection[CONNECTION]
            connection[CONNECTION].commit()
        except DBManagerError:
            connection[CONNECTION].roolback()
            self._close_connection(connection)
        if connection[CREATE_TIME] + self.lifetime < time.time():
            self._return_connection(connection)
        else:
            self._close_connection(connection)

    @contextmanager
    def get_cursor(self):
        '''Context manager for getting cursor.'''
        with self.lock:
            connection = self._get_connection()
            cursor = connection[CONNECTION].cursor(DictCursor)
        try:
            yield cursor
            connection[CONNECTION].commit()
        except DBManagerError:
            connection[CONNECTION].roolback()
            raise
        if connection[CREATE_TIME] + self.lifetime < time.time():
            self._return_connection(connection)
        else:
            self._close_connection(connection)
