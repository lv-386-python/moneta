""" Module for requests using a pool manager. """

from src.python.core.db import pool_manager as db


# TODO cursor and transaction
# TODO MySQL cursor dict

# TODO manage and transaction

# class DbHelper:
@db.re_request()
def select_sql(sql_query):
    """
    Makes SELECT SQL request using a pool manager.
    :params sql_query: sql request
    :return: result of sql request
    """
    with db.pool_manage().manage() as connect:
        # prepare a cursor object using cursor() method
        cursor = connect.cursor() # TODO dict cursor
        # Execute the SQL command
        cursor.execute(sql_query)
        # TODO # pylint: disable=fixme
        # delete before commit
        print(sql_query)
        # Fetch all the rows in a list of lists.
        return cursor.fetchall()


# TODO transaction???
#     def _make_transaction_insert_update_delete_sql(sql_query):

@db.re_request()
def insert_update_delete_sql(sql_query):
    """
    Makes INSERT, UPDATE, DELETE SQL request using a pool manager.
    :params sql_query: sql request
    """
    with db.pool_manage().manage() as connect:
        # prepare a cursor object using cursor() method
        cursor = connect.cursor()
        # Execute the SQL command
        cursor.execute(sql_query)
