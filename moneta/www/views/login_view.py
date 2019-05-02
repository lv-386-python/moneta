"""
This module is responsible for creating views for logging users and for image a home page
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from forms.login_form import UserLoginForm  # pylint:disable = import-error, no-name-in-module
from src.python.db.current import Current
from src.python.db.expend import Expend
from src.python.db.income import Income
from src.python.db.registration import Registration


@login_required
def home(request):
    """
    View for rendering home page.
    """
    income_list = Income.get_income_list_by_user_id(request.user.id)
    expend_list = Expend.get_expend_list_by_user_id(request.user.id)
    current_list = Current.get_current_list_by_user_id(request.user.id)
    context = {'income_list': income_list, 'current_list': current_list, 'expend_list': expend_list}
    return render(request, 'home.html', context)


@require_http_methods(["POST", "GET"])
def login_view(request):
    """

    :param request:
    :return:
    """

    form = UserLoginForm(request.POST)
    if form.is_valid():
        user = authenticate(email=form['email'].value(), password=form['password'].value())
        login(request, user)
        id_user = Registration.get_user_id(user)
        is_activate = Registration.is_active(id_user)
        if user is not None:
            if is_activate:
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('moneta-home')
            logout_view(request)
        else:
            return HttpResponse(content='Please activate your account!', status=403)
    return render(request, "login_app/login.html", {'form': form})


def logout_view(request):
    """

    :param request:
    :return:
    """
    logout(request)
    return redirect('login')
