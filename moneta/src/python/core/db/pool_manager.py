"""Module with pool manager for creating some pool of connections"""
import threading
import time
from contextlib import contextmanager  # pylint:disable = wrong-import-order

import MySQLdb
from MySQLdb.cursors import DictCursor

from core import utils  # pylint:disable = no-name-in-module
from core.constants import CREATE_TIME, CONNECTION, LAST_UPDATE  # pylint:disable = no-name-in-module, import-error
from core.decorators import singleton  # pylint:disable = no-name-in-module, import-error
from core.utils import get_logger

LOGGER = get_logger(__name__)


class DBManagerError(Exception):
    """
    Error of DB or pool manager.
    """

    def __str__(self):
        return repr("Some troubles with database database")

@singleton
class DBPoolManager:
    """
    Class for managing connections to the DB.
    """

    def __init__(self):
        """
        Creating new instance of DB pool manager.
        """
        data = utils.get_config()
        self.__connection_counter = 0
        self.__pool = []
        self.__lock = threading.RLock()
        self.__database = data['client']['database']
        self.__user = data['client']['user']
        self.__port = data['client']['port']
        self.__password = data['client']['password']
        self.__lifetime = data['client']['lifetime']
        self.__delay = data['client']['delay']
        self.__poolsize = data['client']['poolsize']

    def __del__(self):
        '''Method for deleting connection from memory.'''
        for connect in self.__pool:
            self._close_connection(connect)

    def _create_connection(self):
        """
        Create a new connection.
        :return: new connection to the DB
        """
        connection = MySQLdb.connect(database=self.__database,
                                     user=self.__user,
                                     password=self.__password,
                                     port=self.__port,
                                     charset='utf8')

        self.__connection_counter += 1
        return {CONNECTION: connection,
                LAST_UPDATE: 0,
                CREATE_TIME: time.time()}

    def _get_connection(self):
        """
        Get connection from the connection __pool.
        :return connection: connection from pool
        """
        connect = None
        while not connect:
            if self.__pool:
                connect = self.__pool.pop()
            elif self.__connection_counter < self.__poolsize:
                connect = self._create_connection()
            time.sleep(self.__delay)
        return connect

    def _close_connection(self, connection):
        """
        Close old and useless connection.
        :param connection: connection from closing
        """
        connection[CONNECTION].close()
        self.__connection_counter -= 1

    def _return_connection(self, connection):
        """
        Return connection to the __pool.
        :param connection: DB connection
        """
        connection[LAST_UPDATE] = time.time()
        self.__pool.append(connection)

    @contextmanager
    def get_connect(self):
        """
        Context manager for getting connection.
        :yield connect: connect object from database pool
        """
        with self.__lock:
            connection = self._get_connection()
        try:
            yield connection[CONNECTION]
            connection[CONNECTION].commit()
        except DBManagerError:
            LOGGER.error('Connection %s', DBManagerError)
            connection[CONNECTION].roolback()
            self._close_connection(connection)
        if connection[CREATE_TIME] + self.__lifetime < time.time():
            self._return_connection(connection)
        else:
            self._close_connection(connection)

    @contextmanager
    def get_cursor(self):
        """
        Context manager for getting cursor.
        :yield: cursor object from database pool
        """

        with self.__lock:
            connection = self._get_connection()
            cursor = connection[CONNECTION].cursor(DictCursor)
        try:
            yield cursor
            cursor.close()
            connection[CONNECTION].commit()

        except DBManagerError:
            LOGGER.error('Cursor %s', DBManagerError())
            connection[CONNECTION].roolback()
            raise

        if connection[CREATE_TIME] + self.__lifetime < time.time():
            self._return_connection(connection)
        else:
            self._close_connection(connection)
