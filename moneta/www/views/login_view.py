"""
This module is responsible for creating views for logging users and for image a home page
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from core.utils import get_logger
from db.current import Current
from db.expend import Expend
from db.income import Income
from db.registration import Registration
from forms.login_form import UserLoginForm  # pylint:disable = import-error, no-name-in-module

# pylint:disable-msg = too-many-return-statements
LOG = get_logger(__name__)


@login_required
def home(request):
    """
    View for rendering home page.
    """
    income_list = Income.get_income_list_by_user_id(request.user.id)
    expend_list = Expend.get_expend_list_by_user_id(request.user.id)
    current_list = Current.get_current_list_by_user_id(request.user.id)
    context = {'income_list': income_list, 'current_list': current_list, 'expend_list': expend_list}
    LOG.info("Render home page")
    return render(request, 'home.html', context)


@require_http_methods(["POST", "GET"])  # pylint:disable-msg = too-many-return-statements
def login_view(request):
    """

    :param request:
    :return: template for login
    """
    if request.user.is_authenticated:
        LOG.debug("Redirected authenticated user %s to home after"
                  " trying to get login page", request.user)
        return redirect('moneta-home')

    if request.method == "GET":
        LOG.info("Render login page")
        return render(request, "login_app/login.html", {'form': UserLoginForm()})

    form = UserLoginForm(request.POST)
    if form.is_valid():
        user = authenticate(email=form['email'].value(), password=form['password'].value())
        if not user:
            LOG.warning("User %s doesn't pass the authentication", request.user)
            return render(request, "login_app/login.html", {'form': form,
                                                            "err": 'Incorrect input data'})
        if Registration.is_active(user.id):
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            LOG.info("%s redirect to home page", user)
            return redirect('moneta-home')
        LOG.error("Account isn't activated")
        return render(request, "login_app/login.html", {'form': form,
                                                        "err": 'Please activate your account!'})
    LOG.critical("Invalid UserLoginForm")
    return render(request, "login_app/login.html", {'form': form})


def logout_view(request):
    """

    :param request:
    :return:
    """
    logout(request)
    LOG.info("Logout -> redirect to login page")
    return redirect('login')
