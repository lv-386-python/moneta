""" Module for user settings. """
from MySQLdb._exceptions import IntegrityError
from core.db.db_helper import DbHelper


class UserProfile(DbHelper):
    """Models for updating user password"""

    @staticmethod
    def update_pass(new_password, id_user):
        """Method for updating password"""
        query = "UPDATE auth_user SET password = %s WHERE user_id = %s"
        args = (new_password, id_user)
        try:
            UserProfile._make_transaction(query, args)
        except IntegrityError:
            return False
        return True


    @staticmethod
    def delete_user(id_user):
        """Method for deleting user"""
        query = "DELETE FROM user_settings WHERE id = %s"
        args = (id_user,)
        try:
            UserProfile._make_transaction(query, args)
        except IntegrityError:
            return False
        return True

    @staticmethod
    def update_currency(new_currency, id_user):
        """Method for updating default currency in db"""
        query = "UPDATE user_settings SET def_currency = %s WHERE id = %s"
        args = (new_currency, id_user)
        try:
            UserProfile._make_transaction(query, args)
        except IntegrityError:
            return False
        return True

    @staticmethod
    def check_user_default_currency(id_user):
        """ Method for getting user default currency from db. """
        query = """
            SELECT currency
            FROM currencies c
            LEFT JOIN user_settings us ON c.id = us.def_currency
            WHERE us.id=%s;"""
        args = (id_user,)
        query_result = UserProfile._make_select(query, args)[0]
        return query_result
