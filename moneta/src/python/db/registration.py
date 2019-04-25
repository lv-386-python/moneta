"""

Module for registration
"""
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
        query_result = Registration._make_transaction(query, args)
        return query_result

    @staticmethod
    def check_email(email):
        """Method for checking is new user mail already exist in db"""
        query = """SELECT * FROM auth_user WHERE email = %s;"""
        args = (email,)
        with DBPoolManager().get_connect() as conn:
            cursor = conn.cursor()
            check_email = cursor.execute(query, args)
        return check_email

    @staticmethod
    def get_user_id(email):
        """ Method for getting just registered user id. """
        query = """SELECT user_id FROM auth_user WHERE email = %s;"""
        args = (email,)
        with DBPoolManager().get_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, args)
            get_id = cursor.fetchall()[0][0]
        return get_id

    @staticmethod
    def confirm_user(id_user):
        """ Method for activating users account after registration. """
        query = """
                UPDATE user_settings SET is_activated = 1 WHERE id = %s;
                """
        args = (id_user,)
        with DBPoolManager().get_cursor() as curs:
            curs.execute(query, args)

    @staticmethod
    def is_active(email):
        """ Method for getting information about user activation. """
        query = """SELECT is_activated FROM user_settings WHERE id = %s;"""
        args = (email,)
        with DBPoolManager().get_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, args)
            is_activate = cursor.fetchall()[0][0]
        return is_activate
