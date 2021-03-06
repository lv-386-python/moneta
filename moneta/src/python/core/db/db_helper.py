# pylint: disable=too-few-public-methods
""" Module for requests using a pool manager. """

from MySQLdb.cursors import DictCursor

import core.db.pool_manager as db
from core.decorators import retry_request


class DbHelper():
    """
    Class for interacting with database using a pool manager.
    """

    @staticmethod
    @retry_request()
    def _make_select(sql_query, args=None):
        """
        Makes SELECT SQL request using a pool manager.
        :param sql_query: sql query of request
        :param args: args for request
        :return: list of dicts
        """
        with db.DBPoolManager().get_connect() as connect:
            # prepare a cursor object using cursor() method
            cursor = connect.cursor(DictCursor)
            # Execute the SQL command
            cursor.execute(sql_query, args)
            return cursor.fetchall()

    @staticmethod
    @retry_request()
    def _make_transaction(sql_query, args):
        """
        Makes INSERT, UPDATE, DELETE SQL requests using transaction and a pool manager.
        :param sql_query: sql query of request
        :param args: args for request
        :return: data, if available
        """
        with db.DBPoolManager().get_cursor() as cursor:
            # Execute the SQL command
            cursor.execute(sql_query, args)
            # Fetch all the rows in a list of dicts.
            return cursor.fetchall()

__all__ = ['DbHelper']
