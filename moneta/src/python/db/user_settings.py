""" Module for user settings. """
from core.db.pool_manager import DBPoolManager


class UserProfile:
    """Models for updating user password"""

    @staticmethod
    def execute_query(query):
        "this method execute transaction query via pool_manager"
        with DBPoolManager().get_cursor() as curs:
            curs.execute(query)

    @staticmethod
    def get_from_db(query):
        "this method execute query and return some record from db as tuple of tuples"
        with DBPoolManager().get_connect() as conn:
            curs = conn.cursor()
            curs.execute(query)
        return curs.fetchall()

    @staticmethod
    def update_pass(new_password, id_user):
        """Method for updating password"""
        query = "UPDATE auth_user SET password = '{}' WHERE id = {}".format(new_password, id_user)
        UserProfile.execute_query(query)

    @staticmethod
    def delete_user(id_user):
        """Method for deleting user"""
        query = "DELETE FROM auth_user WHERE id = {}".format(id_user)
        UserProfile.execute_query(query)

    @staticmethod
    def get_default_currencies():
        """Method for getting list of default currencies from db"""
        query = """SHOW COLUMNS FROM user where Field='def_currency'"""
        with DBPoolManager().get_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            currencies = cursor.fetchall()[0][1]
            def_currency = [item[1:-1] for item in currencies[5:-1].split(',')]
        return tuple(enumerate(def_currency))

    @staticmethod
    def update_currency(new_currency, id_user):
        """Method for updating default currency in db"""
        query = "UPDATE user SET def_currency = '{}' WHERE id = {}".format(new_currency, id_user)
        UserProfile.execute_query(query)

    @staticmethod
    def check_default_currency(id_user):
        """Method for checking is new user mail already exist in db"""
        query = """select def_currency from user
           where id = '{}';""".format(id_user)
        with DBPoolManager().get_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            current_currency = cursor.fetchall()[0][0]
        return current_currency
