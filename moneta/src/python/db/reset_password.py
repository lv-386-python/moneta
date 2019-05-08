"""Forgot password views and functions."""

from core import decorators, utils  # pylint:disable = import-error, no-name-in-module
from core.db.db_helper import DbHelper


class ResetPassword(DbHelper):
    """ Class for reseting password."""
    @staticmethod
    @decorators.retry_request()
    def get_list_of_user_emails():
        """
        Find user in database by his email.
        :return: List with all user emails.
        """
        sql_str = """
                  SELECT id, email
                  FROM auth_user
                  """
        query = ResetPassword._make_select(sql_str)
        user_emails = []
        for element in query:
            if "email" in element:
                user_emails.append(element["email"])
        return user_emails

    @staticmethod
    @decorators.retry_request()
    def update_password(user_email):
        """
        Method to find user in database by his email.
        :param user_email: Email from user.
        """
        sql_str = """
                  UPDATE auth_user
                  SET password = %s
                  WHERE email = %s
                  """
        new_user_password = utils.random_string()
        utils.send_email(new_user_password, user_email)
        hashed_password = utils.hash_password(new_user_password)
        args = (hashed_password, user_email)
        ResetPassword._make_transaction(sql_str, args)
