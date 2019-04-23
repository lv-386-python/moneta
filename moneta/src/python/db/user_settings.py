""" Module for user settings. """
from src.python.core.db.pool_manager import DBPoolManager
from src.python.db.currencies import Currency


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
        # """Method for getting list of default currencies from db"""
        get_currency_list = Currency.currency_list()
        list_of_currency = tuple(enumerate(get_currency_list))
        return list_of_currency

    @staticmethod
    def update_currency(new_currency, id_user):
        """Method for updating default currency in db"""
        query = "UPDATE user_settings SET def_currency = %s WHERE id = %s"
        args = (new_currency, id_user)
        with DBPoolManager().get_cursor() as curs:
            curs.execute(query, args)

    @staticmethod
    def check_default_currency(id_user):
        """ Method for checking availability of user with such email in db. """
        query = """
        SELECT currency
        FROM user_settings
        JOIN currencies cs on user_settings.def_currency = cs.id
        WHERE user_settings.id = '{}';""".format(id_user)
        with DBPoolManager().get_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            current_currency = cursor.fetchall()[0][0]
            print(current_currency)
        return current_currency
