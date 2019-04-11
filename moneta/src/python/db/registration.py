"""
Module for registration
"""
from src.python.core.db.pool_manager import DBPoolManager


class Registration:
    """Class for creating registration"""

    @staticmethod
    def sign_up(password, email, currency, active):
        """Method for saving data about new user in table auth_user"""
        query = """
            INSERT INTO auth_user (password, email) values (%s, %s);
            INSERT INTO user (id, def_currency, is_activated) values (LAST_INSERT_ID(), %s, %s);
             """
        args = (password, email, currency, active)
        with DBPoolManager().get_cursor() as curs:
            curs.execute(query, args)

    @staticmethod
    def check_email(email):
        """Method for checking is new user mail already exist in db"""
        query = """select * from auth_user where email = %s;"""
        args = (email,)
        with DBPoolManager().get_connect() as conn:
            cursor = conn.cursor()
            check_email = cursor.execute(query, args)
        return check_email
