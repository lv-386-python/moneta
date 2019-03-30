import MySQLdb
import threading
import functools
import time
import logging
logging.basicConfig(filename='pool2.log', filemode="w", level=logging.DEBUG)
from contextlib import contextmanager


DEFAULT_COUNTER = 5
DEFAULT_WAIT_TIME = 1
DELAY = 0.01
DB_POOL = {'DB': None}
DB_POOL_LOCK = {'TH': threading.RLock()}


CONNECT_SETTINGS = {'db': 'db_moneta',
                    'username': 'moneta_user',
                    'password': 'db_password',
                    'default-character-set': 'utf8',
                    'port': 3806,
                    'host': 'localhost',
                    'life_time': 1,
                    'pool_size': 10
                   }

class Singleton(type):
    """
    using a Singleton pattern to work with only one possible instance of Pool
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

class DBManagerError(MySQLdb.Error):
    pass


def re_request(counter=DEFAULT_COUNTER, wait_time=DEFAULT_WAIT_TIME):
    logging.info('all is _ok')

    def re_request_wrapper(func):
        @functools.wraps(func)
        def iner(*args, **kwargs):
            wr_counter, wait = counter, wait_time
            while wr_counter:
                try:
                    logging.info('try to return')
                    return func(*args, **kwargs)
                except Exception:
                    logging.info('Error in wrapper')
                    if wr_counter:
                        time.sleep(wait)
                    else:
                        raise DBManagerError
                logging.info('counter decrise')
                wr_counter -= 1
        return iner
    return re_request_wrapper


class DBPoolManager:
    def __init__(self, username, password, db, host, port , life_time, pool_size):
        # logging.info('57 method.init')
        self.username = username
        self.password = password
        self.db = db
        self.host = host
        self.port = port
        self.life_time = life_time
        self.pool_size = pool_size
        self.connection_counter = 0
        self.pool = []
        self.lock = threading.RLock()
        

    def __del__(self):
        # logging.info('74 method.delete')
        for connect in self.pool:
            self.close_connection(connect)

    def create_connection(self):
        # logging.info('79 method.create')
        connection = MySQLdb.connect(user=self.username,
                                     password=self.password,
                                     db=self.db,
                                     host=self.host,
                                     port=self.port,
                                     charset='utf8',
                                     init_command='SET NAMES UTF8')
        return {'connection': connection,
                'last_update': 0,
                'create_time': time.time()}

    def get_connection(self):
        # logging.info('92 method.get')
        
        connect = None
        while not connect:
            if self.pool:
                connect = self.pool.pop()
            elif self.connection_counter < self.pool_size:
                connect = self.create_connection()
                self.connection_counter += 1
            time.sleep(DELAY)
        return connect

    def close_connection(self, connection):
        # logging.info('105 method.close')
        self.connection_counter -= 1
        connection['connection'].close()

    def return_connection(self, connection):
        # logging.info('110 method.return')
        connection['last_update'] = time.time
        self.pool.append(connection)

    @contextmanager
    def manage(self):
        # logging.info('116 manager')
        with self.lock:
            connection = self.get_connection()
        try:
            yield connection['connection']
        except Exception:
            self.close_connection(connection)
        if connection['create_time'] + self.life_time < time.time():
            self.return_connection(connection)
        else:
            self.close_connection(connection)

    @contextmanager
    def transaction(self):
        # logging.info('130 method.transaction')
        with self.lock:
            connection = self.get_connection()
            cursor = connection['connection'].cursor()
        try:
            yield cursor
            connection['connection'].commit()
        except Exception:
            connection['connection'].roolback()
            raise
        if connection['create_time'] + self.life_time < time.time():
            self.return_connection(connection)
        else:
            self.close_connection(connection)


def pool_manage():
    # logging.info('147 used pool manager')
    if DB_POOL['DB'] is None:
        with DB_POOL_LOCK['TH']:
            if DB_POOL['DB'] is None:
                DB_POOL['DB'] = DBPoolManager(db='db_moneta',
                                        username='moneta_user',
                                        password='db_password',
                                        port=3806,
                                        host='localhost',
                                        life_time=1,
                                        pool_size=10
                                        )
    return DB_POOL['DB']    # logging.info('used pool manager')
    # used_pool = DBPoolManager(db='db_moneta',
    #                           username='moneta_user',
    #                           password='db_password',
    #                           port=3806,
    #                           host='localhost',
    #                           life_time=1,
    #                           pool_size=10
    #                          )
    # logging.info('all is ok')

    # return used_pool
