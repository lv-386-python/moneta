from django.shortcuts import render
from django.core.mail import send_mail
from authentication import reset_password


import random
import string

def randomString(stringlength=10):
    """Generate a random string of fixed length """
    password = string.ascii_lowercase
    return ''.join(random.choice(password) for i in range(stringlength))

def have_email_from_user(request):
    """Get user email"""
    if request.method == "POST":
        try:
            USER_EMAIL = request.POST.get('email')
        except (ValueError):
            pass
        return USER_EMAIL

def user_not_exist(request):
    """ Check if user does not exist """
    if request.method == "POST":
        try:
            email_user = have_email_from_user(request)
            have_sql = reset_password.find_user_in_database(email_user)
        except (ValueError):
            pass
        if not have_sql:
            have_sql = None
            return have_sql
        else:
            return have_sql

def send_email(new_password, USER_EMAIL):
    """ Send a messsage to user"""
    try:
        #need to add USER_EMAIL as our_user
        print("mail was successfully sended")
        send_mail('TESTIK',
                  f'HELLO ! Your new password is  {new_password}',
                  'lvmoneta386@gmail.com',
                  [USER_EMAIL] )
    except (ValueError):
        pass


def reset_user_password(request):
    """ View to reset user password"""
    if request.method == "POST":
        try:
            user_response = user_not_exist(request)
            if user_response:
                new_user_password = randomString()
                password = reset_password.save_password_in_db(user_response, new_user_password)
                send_email(password,user_response)
                return render(request, "valid_email.html")
            else:
                return render(request, "not_user.html")
        except (ValueError):
            pass
    return render(request, "forgot_password.html")





