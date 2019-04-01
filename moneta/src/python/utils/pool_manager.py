'''_pool manager module'''
from contextlib import contextmanager
import time
import threading
import functools
import MySQLdb


LAST_UPDATE = 'last_update'
CREATE_TIME = 'create_time'
CONNECTION = 'connection'
DEFAULT_COUNTER = 5
DEFAULT_WAIT_TIME = 1
DELAY = 0.01
DATA_BASE = 'DB'
THREAD_LOCK = 'TH'
DB_POOL = {DATA_BASE: None}
DB_POOL_LOCK = {THREAD_LOCK: threading.RLock()}
CONNECT_SETTINGS = {'data_base': 'db_moneta',
                    'username': 'moneta_user',
                    'password': 'db_password',
                    'port': 3806,
                    'host': 'localhost',
                    'life_time': 1,
                    'pool_size': 10
                   }


class DBManagerError(Exception):
    '''Error "full _pool" or ""'''


def re_request(counter=DEFAULT_COUNTER, wait_time=DEFAULT_WAIT_TIME):
    '''Decorator for resendings requests to the DB'''
    def re_request_wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            wr_counter, wait = counter, wait_time
            while wr_counter:
                try:
                    return func(*args, **kwargs)
                except DBManagerError:
                    if wr_counter:
                        time.sleep(wait)
                    else:
                        raise DBManagerError
                wr_counter -= 1
        return inner
    return re_request_wrapper


class DBPoolManager:
    '''Class for managing connections to the DB'''
    def __init__(self, username, password, data_base, host, port, life_time, pool_size):
        '''creating new instance of DB _pool manager'''
        self.username = username
        self.password = password
        self.data_base = data_base
        self.host = host
        self.port = port
        self.life_time = life_time
        self.pool_size = pool_size
        self._connection_counter = 0
        self._pool = []
        self.lock = threading.RLock()

    def __del__(self):
        '''method for deleting connection from memory'''
        for connect in self._pool:
            self._close_connection(connect)

    def _create_connection(self):
        '''create a new connection'''
        connection = MySQLdb.connect(user=self.username,
                                     password=self.password,
                                     db=self.data_base,
                                     host=self.host,
                                     port=self.port,
                                     charset='utf8',
                                     init_command='SET NAMES UTF8')
        return {CONNECTION: connection,
                LAST_UPDATE: 0,
                CREATE_TIME: time.time()}

    def _get_connection(self):
        '''get connection from the connection _pool'''
        connect = None
        while not connect:
            if self._pool:
                connect = self._pool.pop()
            elif self._connection_counter < self.pool_size:
                connect = self._create_connection()
                self._connection_counter += 1
            time.sleep(DELAY)
        return connect

    def _close_connection(self, connection):
        '''close old and uselese connection'''
        self._connection_counter -= 1
        connection[CONNECTION].close()

    def _return_connection(self, connection):
        '''return connection to the _pool'''
        connection[LAST_UPDATE] = time.time
        self._pool.append(connection)

    @contextmanager
    def manage(self):
        '''context manager for solo query manipulation'''
        with self.lock:
            connection = self._get_connection()
        try:
            yield connection[CONNECTION]
        except DBManagerError:
            self._close_connection(connection)
        if connection[CREATE_TIME] + self.life_time < time.time():
            self._return_connection(connection)
        else:
            self._close_connection(connection)

    @contextmanager
    def transaction(self):
        '''context manager for making transaction'''
        with self.lock:
            connection = self._get_connection()
            cursor = connection[CONNECTION].cursor()
        try:
            yield cursor
            connection[CONNECTION].commit()
        except DBManagerError:
            connection[CONNECTION].roolback()
            raise
        if connection[CREATE_TIME] + self.life_time < time.time():
            self._return_connection(connection)
        else:
            self._close_connection(connection)


def pool_manage():
    '''fucntion for creating data base _pool manager'''
    if DB_POOL[DATA_BASE] is None:
        with DB_POOL_LOCK[THREAD_LOCK]:
            if DB_POOL[DATA_BASE] is None:
                DB_POOL[DATA_BASE] = DBPoolManager(**CONNECT_SETTINGS)
    return DB_POOL[DATA_BASE]
