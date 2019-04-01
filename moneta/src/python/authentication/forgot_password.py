"""forgot password views and functions"""
import random
import string
from django.shortcuts import render
from django.core.mail import send_mail
from authentication import reset_password


def random_string(stringlength=10):
    """Generate a random string of fixed length"""
    password = string.ascii_lowercase
    return ''.join(random.choice(password) for i in range(stringlength))

def send_email(new_password, user_email):
    """Send a messsage to user"""
    try:
        print("mail was successfully sended")
        send_mail('TESTIK',
                  f'HELLO ! Your new password is  {new_password}',
                  'lvmoneta386@gmail.com',
                  [user_email])
    except ValueError:
        pass

def have_email_from_user(request):
    """Get user email"""
    if request.method == "POST":
        try:
            user_email = request.POST.get('email')
        except ValueError:
            pass
        return user_email

def user_not_exist(request):
    """Check if user does not exist"""
    if request.method == "POST":
        try:
            email_user = have_email_from_user(request)
            have_sql = reset_password.find_user_in_database(email_user)
        except ValueError:
            pass
        if not have_sql:
            have_sql = None
        return have_sql

def reset_user_password(request):
    """View to reset user password"""
    if request.method == "POST":
        try:
            user_response = user_not_exist(request)
            if user_response:
                new_user_password = random_string()
                password = reset_password.save_password_in_db(user_response, new_user_password)
                send_email(password, user_response)
                return render(request, "authentication/valid_email.html")
            else:
                return render(request, "authentication/not_user.html")
        except ValueError:
            pass
    return render(request, "authentication/forgot_password.html")
