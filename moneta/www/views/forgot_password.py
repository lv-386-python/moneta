"""View to reset user password."""
from django.shortcuts import render
from src.python.db import reset_password


def have_email_from_user(request):
    """Get user email."""
    if request.method == "POST":
        try:
            user_email = request.POST.get('email')
        except ValueError:
            return None
    return user_email

def reset_user_password(request):
    """View to reset user password."""
    if request.method == "POST":
        try:
            user_response = reset_password.user_exists(request)
            if user_response:
                return render(request, "authentication/valid_email.html")
            return render(request, "authentication/not_user.html")
        except ValueError:
            return render(request, "authentication/not_user.html")
    return render(request, "authentication/forgot_password.html")
