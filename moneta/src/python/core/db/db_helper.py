# pylint: disable=too-few-public-methods
""" Module for requests using a pool manager. """

import core.db.pool_manager as db
from core.decorators import retry_request


class DbHelper:
    """
    Class for interacting with database using a pool manager.
    """
    @staticmethod
    @retry_request()
    def _make_select(sql_query):
        """
        Makes SELECT SQL request using a pool manager.
        :params sql_query: sql request
        :return: list of dicts
        """
        with db.DBPoolManager().get_cursor() as cursor:
            # Execute the SQL command
            cursor.execute(sql_query)
            # Fetch all the rows in a list of dicts.
            return cursor.fetchall()

    @staticmethod
    @retry_request()
    def _make_transaction(sql_query):
        """
        Makes INSERT, UPDATE, DELETE SQL requests using transaction and a pool manager.
        :params sql_query: sql request
        :return: data, if available
        """
        with db.DBPoolManager().get_connect() as connect:
            # prepare a cursor object using cursor() method
            cursor = connect.cursor()
            # Execute the SQL command
            cursor.execute(sql_query)
            return cursor.fetchall()
