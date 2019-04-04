"""View to reset user password."""
from django.shortcuts import render
from src.python.core import generate_password, send_new_password
from src.python.db import reset_password

def reset_user_password(request):
    """View to reset user password."""
    if request.method == "POST":
        try:
            user_response = reset_password.user_not_exist(request)
            if user_response:
                new_user_password = generate_password.random_string()
                password = reset_password.save_password_in_db(user_response, new_user_password)
                send_new_password.send_email(password, user_response)
                return render(request, "authentication/valid_email.html")
            return render(request, "authentication/not_user.html")
        except ValueError:
            return render(request, "authentication/not_user.html")
    return render(request, "authentication/forgot_password.html")
