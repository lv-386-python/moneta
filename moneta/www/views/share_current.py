"""View to reset user password."""
from django.shortcuts import render
from src.python.db import reset_password

def share_current(request):
    """View to reset user password."""
    return render(request, "current/share_current.html")