"""functions to reset password"""
from helper import pool_manager as db

@db.re_request()
def find_user_by_email(our_user):
    """Find user in database by his email"""
    try:
        query = f"Select id, email from user where email = '{our_user}'"
        with db.pool_manage().manage() as connect:
            cursor = connect.cursor()
            cursor.execute(query)
            sql_str = cursor.fetchall()  # make a list from sets
    except ValueError:
        pass
    if not sql_str:
        return None
    else:
        return our_user

@db.re_request()
def save_password_in_db(our_user, new_password):
    """Update user password"""
    try:
        changed_password = f"UPDATE user SET password = '{new_password}' WHERE email = '{our_user}'"
        with db.pool_manage().manage() as connect:
            cursor = connect.cursor()
            cursor.execute(changed_password)
    except ValueError:
        pass
    return new_password
