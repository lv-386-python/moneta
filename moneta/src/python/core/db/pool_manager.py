'''_module with decorator for repeate try of getting connection from the pool
 and pool manager for creating some pool of connections'''
from contextlib import contextmanager
import time
import threading
import MySQLdb
from MySQLdb.cursors import DictCursor
from src.python.core import utils
from src.python.core.constants import CREATE_TIME, CONNECTION, LAST_UPDATE
from src.python.core.decorators import singleton


DATA_CONF = utils.get_db_config()


class DBManagerError(Exception):
    '''Error of DB or pool manager.'''


@singleton
class DBPoolManager:
    '''Class for managing connections to the DB'''
    def __init__(self):
        '''creating new instance of DB _pool manager'''
        self._connection_counter = 0
        self._pool = []
        self.lock = threading.RLock()

    def __del__(self):
        '''method for deleting connection from memory'''
        for connect in self._pool:
            self._close_connection(connect)

    def _create_connection(self):
        '''create a new connection'''
        connection = MySQLdb.connect(database=DATA_CONF['database'],
                                     user=DATA_CONF['user'],
                                     password=DATA_CONF['password'],
                                     port=DATA_CONF['port'])
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
            elif self._connection_counter < DATA_CONF['poolsize']:
                connect = self._create_connection()
            time.sleep(DATA_CONF['delay'])
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
    def manage(self):
        '''context manager for solo query manipulation'''
        with self.lock:
            connection = self._get_connection()
        try:
            yield connection[CONNECTION]
            connection[CONNECTION].commit()
        except DBManagerError:
            connection[CONNECTION].roolback()
            self._close_connection(connection)
        if connection[CREATE_TIME] + DATA_CONF['lifetime'] < time.time():
            self._return_connection(connection)
        else:
            self._close_connection(connection)

    @contextmanager
    def transaction(self):
        '''context manager for making transaction'''
        with self.lock:
            connection = self._get_connection()
            cursor = connection[CONNECTION].cursor(DictCursor)
        try:
            yield cursor
            connection[CONNECTION].commit()
        except DBManagerError:
            connection[CONNECTION].roolback()
            raise
        if connection[CREATE_TIME] + DATA_CONF['lifetime'] < time.time():
            self._return_connection(connection)
        else:
            self._close_connection(connection)


def pool_manage():
    '''fucntion for creating data base _pool manager'''
    return DBPoolManager()
