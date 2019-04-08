"""Forgot password views and functions."""
from core.db import pool_manager as db # pylint:disable = import-error, no-name-in-module
from core import decorators, utils # pylint:disable = import-error, no-name-in-module
from views import forgot_password # pylint:disable = import-error, no-name-in-module


class ResetPassword():
    """ Class for reseting password."""
    @staticmethod
    @decorators.retry_request()
    def find_user_by_email(user_email):
        """Find user in database by his email."""
        query = f"Select id, email from auth_user where email = '{user_email}'"
        with db.DBPoolManager().get_connect() as connect:
            cursor = connect.cursor()
            cursor.execute(query)
            sql_str = cursor.fetchall()
        if not sql_str:
            return None
        return user_email

    @staticmethod
    @decorators.retry_request()
    def save_password_in_db(user_email, new_password):
        """Update user password."""
        changed_password = f"UPDATE auth_user SET password = '{new_password}'" \
            f" WHERE email = '{user_email}'"
        with db.DBPoolManager().get_connect() as connect:
            cursor = connect.cursor()
            cursor.execute(changed_password)
        return new_password

def user_exists(request):
    """Check if user does not exist."""
    if request.method == "POST":
        try:
            user = ResetPassword()
            user_email = forgot_password.have_email_from_user(request)
            have_sql = user.find_user_by_email(user_email)
        except ValueError:
            return None
        if not have_sql:
            have_sql = None
        else:
            new_user_password = utils.random_string()
            password = user.save_password_in_db(user_email, new_user_password)
            utils.send_email(password, user_email)
    return have_sql
