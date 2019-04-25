""" Module for user settings. """
from src.python.core.db.pool_manager import DBPoolManager
from core.db.db_helper import DbHelper


class UserProfile(DbHelper):
    """Models for updating user password"""

    @staticmethod
    def update_pass(new_password, id_user):
        """Method for updating password"""
        query = "UPDATE auth_user SET password = %s WHERE user_id = %s"
        args = (new_password, id_user)
        query_result = UserProfile._make_transaction(query, args)
        return query_result

    @staticmethod
    def delete_user(id_user):
        """Method for deleting user"""
        query = "DELETE FROM user_settings WHERE id = %s"
        args = (id_user,)
        query_result = UserProfile._make_transaction(query, args)
        return query_result

    @staticmethod
    def update_currency(new_currency, id_user):
        """Method for updating default currency in db"""
        query = "UPDATE user_settings SET def_currency = %s WHERE id = %s"
        args = (new_currency, id_user)
        query_result = UserProfile._make_transaction(query, args)
        return query_result

    @staticmethod
    def check_user_default_currency(id_user):
        """ Method for getting user default currency from db. """
        query = """
        SELECT currency
        FROM user_settings
        JOIN currencies cs on user_settings.def_currency = cs.id
        WHERE user_settings.id = '{}';""".format(id_user)
        with DBPoolManager().get_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            current_currency = cursor.fetchall()[0][0]
        return current_currency
