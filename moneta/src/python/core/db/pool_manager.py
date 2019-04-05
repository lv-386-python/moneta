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
    '''Class for managing connections to the DB.'''
    def __init__(self):
        '''Creating new instance of DB pool manager.'''
        data = utils.get_config()
        self.__connection_counter = 0
        self.__pool = []
        self.__lock = threading.RLock()
        self.__database = data['moneta']['database']
        self.__user = data['moneta']['user']
        self.__port = data['moneta']['port']
        self.__password = data['moneta']['password']
        self.__lifetime = data['moneta']['lifetime']
        self.__delay = data['moneta']['delay']
        self.___poolsize = data['moneta']['poolsize']

    def __del__(self):
        '''Method for deleting connection from memory.'''
        for connect in self.__pool:
            self._close_connection(connect)

    def _create_connection(self):
        '''Create a new connection.'''
        connection = MySQLdb.connect(database=self.__database,
                                     user=self.__user,
                                     password=self.__password,
                                     port=self.__port)
        self.__connection_counter += 1
        return {CONNECTION: connection,
                LAST_UPDATE: 0,
                CREATE_TIME: time.time()}

    def _get_connection(self):
        '''Get connection from the connection __pool.'''
        connect = None
        while not connect:
            if self.__pool:
                connect = self.__pool.pop()
            elif self.__connection_counter < self.___poolsize:
                connect = self._create_connection()
            time.sleep(self.__delay)
        return connect

    def _close_connection(self, connection):
        '''Close old and uselese connection.'''
        connection[CONNECTION].close()
        self.__connection_counter -= 1

    def _return_connection(self, connection):
        '''Return connection to the __pool.'''
        connection[LAST_UPDATE] = time.time()
        self.__pool.append(connection)

    @contextmanager
    def get_connect(self):
        '''Context manager for getting connection.'''
        with self.__lock:
            connection = self._get_connection()
        try:
            yield connection[CONNECTION]
            connection[CONNECTION].commit()
        except DBManagerError:
            connection[CONNECTION].roolback()
            self._close_connection(connection)
        if connection[CREATE_TIME] + self.__lifetime < time.time():
            self._return_connection(connection)
        else:
            self._close_connection(connection)

    @contextmanager
    def get_cursor(self):
        '''Context manager for getting cursor.'''

        with self.__lock:
            connection = self._get_connection()
            cursor = connection[CONNECTION].cursor(DictCursor)
        try:
            yield cursor
            connection[CONNECTION].commit()
        except DBManagerError:
            connection[CONNECTION].roolback()
            raise
        if connection[CREATE_TIME] + self.__lifetime < time.time():
            self._return_connection(connection)
        else:
            self._close_connection(connection)
