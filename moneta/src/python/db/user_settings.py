""" Module for user settings. """
from src.python.core.db.pool_manager import DBPoolManager


class UserProfile:
    """Models for updating user password"""

    @staticmethod
    def update_pass(new_password, id_user):
        """Method for updating password"""
        query = "UPDATE auth_user SET password = %s WHERE id = %s"
        args = (new_password, id_user)
        with DBPoolManager().get_cursor() as curs:
            curs.execute(query, args)

    @staticmethod
    def delete_user(id_user):
        """Method for deleting user"""
        query = "DELETE FROM auth_user WHERE id = %s"
        args = (id_user,)
        with DBPoolManager().get_cursor() as curs:
            curs.execute(query, args)

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
        query = "UPDATE user SET def_currency = %s WHERE id = %s"
        args = (new_currency, id_user)
        with DBPoolManager().get_cursor() as curs:
            curs.execute(query, args)

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
