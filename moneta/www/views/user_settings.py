"""Modules for user settings"""
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
from src.python.db.user_settings import UserProfile

from www.views.login_view import logout_view
from www.forms.user_settings import ChangePasswordForm, ChangeCurrencyForm


def user_settings(request):
    """
    Page with settings, no other functional
    """
    return render(request, 'user_profile/user_settings.html')


def change_password(request):
    """Method for changing password"""
    user = request.user
    id_user = request.user.id
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            check_pass = request.user.check_password(old_password)
            if check_pass:
                confirm_pass = form.cleaned_data.get('confirm_pass')
                if new_password == confirm_pass:
                    user.set_password(new_password)
                    new_password = user.password
                    UserProfile.update_pass(new_password, id_user)
                    messages.success(request, 'Password successfully updated!')
                    update_session_auth_hash(request, user)
                else:
                    messages.error(request, 'Error with new pass confirmation!')
            else:
                messages.error(request, "Something wrong with your passwords!")
        else:
            messages.error(request, 'Your form is not valid!.')
    else:
        form = ChangePasswordForm()
    return render(request, 'user_profile/change_password.html', {'form': form})


def delete_user(request):
    """ Method for deleting user. """
    if request.method == 'POST':
        id_user = request.user.id
        UserProfile.delete_user(id_user)
        messages.success(request, 'Your account was successfully deleted!')
        logout_view(request)
    return render(request, 'user_profile/delete_user.html')


def change_currency(request):
    """ Method for changing currencies. """
    id_user = request.user.id
    user = request.user
    if request.method == 'POST':
        form = ChangeCurrencyForm(request.POST)
        if form.is_valid():
            id_currency = int(form.cleaned_data.get('select_default_currency'))
            id_currency += 1
            UserProfile.update_currency(id_currency, id_user)
            messages.success(request, 'Default currency successfully updated!')
            update_session_auth_hash(request, user)
        else:
            messages.error(request, 'You must choose currency!')
    else:
        form = ChangeCurrencyForm()
    current_currency = UserProfile.check_default_currency(id_user)
    context = {'current_currency': current_currency, 'form': form}
    return render(request, 'user_profile/change_currency.html', context)
