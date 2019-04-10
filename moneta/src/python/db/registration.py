"""
Module for registration
"""
from core.db.pool_manager import DBPoolManager


class Registration:
    """Class for creating registration"""

    @staticmethod
    def execute_query(query):
        """ This method execute transaction query via pool_manager. """
        with DBPoolManager().get_cursor() as curs:
            curs.execute(query)

    @staticmethod
    def sign_up(password, email):
        """Method for saving data about new user in table auth_user"""
        query = """
            INSERT INTO auth_user (password, email)
            values ('{}', '{}');""".format(password, email)
        Registration.execute_query(query)

    @staticmethod
    def set_currency(currency, active):
        """Method for saving data about new user in table user"""
        query = """INSERT INTO user (def_currency, is_activated)
            values ('{}', {});""".format(currency, active)
        Registration.execute_query(query)

    @staticmethod
    def check_email(email):
        """Method for checking is new user mail already exist in db"""
        query = """select 1 from user
            where not exists (select 1 from auth_user where email = '{}');""".format(email)
        with DBPoolManager().get_connect() as conn:
            cursor = conn.cursor()
            check_email = cursor.execute(query)
        return check_email
