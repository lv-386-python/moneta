from helper import pool_manager as db


@db.re_request()
def select_sql(sql_query):
    """
    Makes SELECT SQL request using a pool manager.
    :params sql_query: sql request
    :return: result of sql request
    """
    with db.pool_manage().manage() as connect:
        # prepare a cursor object using cursor() method
        cursor = connect.cursor()
        # Execute the SQL command
        cursor.execute(sql_query)
        # Fetch all the rows in a list of lists.
        return cursor.fetchall()


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
