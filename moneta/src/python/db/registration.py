"""

Module for registration
"""
from MySQLdb._exceptions import IntegrityError
from core.db.db_helper import DbHelper

from src.python.core.db.pool_manager import DBPoolManager


class Registration(DbHelper):
    """Class for creating registration"""

    @staticmethod
    def save_data(currency, active, password, email):
        """Method for saving data about new user in table auth_user"""
        query = """
            START TRANSACTION;
            INSERT INTO user_settings (def_currency, is_activated) VALUES (%s, %s);
            INSERT INTO auth_user (user_id, password, email)
            VALUES ((SELECT MAX(id) from user_settings), %s, %s);
            COMMIT;
             """
        args = (currency, active, password, email)
        try:
            Registration._make_transaction(query, args)
        except IntegrityError:
            return False
        return True

    @staticmethod
    def email_exist_id_db(email):
        """Method for checking is new user mail already exist in db"""
        query = """SELECT * FROM auth_user WHERE email = %s;"""
        args = (email,)
        try:
            Registration._make_select(query, args)
        except IntegrityError:
            return False
        return True

    @staticmethod
    def get_user_id(email):
        """ Method for getting just registered user id. """
        query = """SELECT user_id FROM auth_user WHERE email = %s;"""
        args = (email,)
        try:
            Registration._make_select(query, args)[0]['user_id']
        except IntegrityError:
            return False
        return True

    @staticmethod
    def confirm_user(id_user):
        """ Method for activating users account after registration. """
        query = """
                UPDATE user_settings SET is_activated = 1 WHERE id = %s;
                """
        args = (id_user,)
        try:
            Registration._make_transacrion(query, args)
        except IntegrityError:
            return False
        return True

    @staticmethod
    def is_active(id_user):
        """ Method for getting information about user activation. """
        query = """SELECT is_activated FROM user_settings WHERE id = %s;"""
        args = (id_user,)
        try:
            Registration._make_select(query, args)[0]['is_activated']
        except IntegrityError:
            return False
        return True
