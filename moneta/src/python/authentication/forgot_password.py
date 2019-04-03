"""Forgot password views and functions."""
import random
import string
from django.shortcuts import render
from django.core.mail import send_mail

try:
    from helper import pool_manager as db
except ImportError:
    pass

def have_email_from_user(request):
    """Get user email."""
    if request.method == "POST":
        try:
            user_email = request.POST.get('email')
        except ValueError:
            return None
    return user_email

def random_string(stringlength=10):
    """Generate a random string of fixed length."""
    password = string.ascii_lowercase
    return ''.join(random.choice(password) for i in range(stringlength))

@db.re_request()
def find_user_by_email(user_email):
    """Find user in database by his email."""
    try:
        query = f"Select id, email from user where email = '{user_email}'"
        with db.pool_manage().manage() as connect:
            cursor = connect.cursor()
            cursor.execute(query)
            sql_str = cursor.fetchall()
    except ValueError:
        return None
    if not sql_str:
        return None
    return user_email

@db.re_request()
def save_password_in_db(user_email, new_password):
    """Update user password."""
    try:
        changed_password = f"UPDATE user SET password = '{new_password}' WHERE email = '{user_email}'"
        with db.pool_manage().manage() as connect:
            cursor = connect.cursor()
            cursor.execute(changed_password)
    except ValueError:
        return None
    return new_password

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


def send_email(new_password, user_email):
    """Send a messsage to user."""
    try:
        send_mail('no reply',
                  f'HELLO from "Moneta"! Your new password is  {new_password}',
                  'lvmoneta386@gmail.com',
                  [user_email])
    except ValueError:
        pass

def reset_user_password(request):
    """View to reset user password."""
    if request.method == "POST":
        try:
            user_response = user_not_exist(request)
            if user_response:
                new_user_password = random_string()
                password = save_password_in_db(user_response, new_user_password)
                send_email(password, user_response)
                return render(request, "authentication/valid_email.html")
            return render(request, "authentication/not_user.html")
        except ValueError:
            return render(request, "authentication/not_user.html")
    return render(request, "authentication/forgot_password.html")
