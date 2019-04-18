"""
This module is responsible for creating views for logging users and for image a home page
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from www.forms.login_form import UserLoginForm  # pylint:disable = import-error, no-name-in-module


@login_required
def home(request):
    """

    :param request:
    :return:
    """


    return render(request, 'home.html')


def login_view(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form['email'].value(), password=form['password'].value())

            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('moneta-home')
    else:
        form = UserLoginForm()
    return render(request, "login_app/login.html", {'form': form})


def logout_view(request):
    """

    :param request:
    :return:
    """
    logout(request)
    return redirect('login')
