"""Forgot password views and functions."""
from src.python.core.db import pool_manager as db

def have_email_from_user(request):
    """Get user email."""
    if request.method == "POST":
        try:
            user_email = request.POST.get('email')
        except ValueError:
            return None
    return user_email

@db.re_request()
def find_user_by_email(user_email):
    """Find user in database by his email."""
    try:
        query = f"Select id, email from auth_user where email = '{user_email}'"
        with db.pool_manage().manage() as connect:
            cursor = connect.cursor()
            cursor.execute(query)
            sql_str = cursor.fetchall()
    except ValueError:
        return None
    if not sql_str:
        return None
    return user_email

def user_not_exist(request):
    """Check if user does not exist."""
    if request.method == "POST":
        try:
            email_user = have_email_from_user(request)
            have_sql = find_user_by_email(email_user)
        except ValueError:
            return None
        if not have_sql:
            have_sql = None
    return have_sql

@db.re_request()
def save_password_in_db(user_email, new_password):
    """Update user password."""
    try:
        changed_password = f"UPDATE auth_user SET password = '{new_password}'" \
            f" WHERE email = '{user_email}'"
        with db.pool_manage().manage() as connect:
            cursor = connect.cursor()
            cursor.execute(changed_password)
    except ValueError:
        return None
    return new_password
