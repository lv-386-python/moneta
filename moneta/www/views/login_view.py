"""
This module is responsible for creating views for logging users and for image a home page
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from forms.login_form import UserLoginForm  # pylint:disable = import-error, no-name-in-module
from src.python.db.current import Current
from src.python.db.expend import Expend
from src.python.db.income import Income


@login_required
def home(request):
    """
    View for rendering home page.
    """
    income_list = Income.get_income_list_by_user_id(request.user.id)
    print(income_list)
    expend_list = Expend.get_expend_list_by_user_id(request.user.id)
    current_list = Current.get_current_list_by_user_id(request.user.id)
    context = {'income_list': income_list, 'current_list': current_list, 'expend_list': expend_list}
    return render(request, 'home.html', context)


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
