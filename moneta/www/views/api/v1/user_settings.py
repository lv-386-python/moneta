"""Modules for user settings"""
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.http.request import QueryDict
from django.views.decorators.http import require_http_methods

from core.utils import get_logger
from src.python.db.registration import Registration
from src.python.db.user_settings import UserProfile
from www.forms.user_settings import ChangePasswordForm, ChangeCurrencyForm
from www.views.login_view import logout_view

LOGGER = get_logger(__name__)


@login_required
@require_http_methods(["GET"])
def user_settings(request):
    """
        Page with settings, no other functional
        """
    if request.method == "GET":
        id_user = request.user.id
        email = Registration.get_user_email(id_user)
        current_currency = UserProfile.check_user_default_currency(id_user)
        cont = {**current_currency, **email}
        LOGGER.debug("Returned JSON with default settings for user %s", request.user)
        return JsonResponse(cont, safe=False)
    LOGGER.warning("Method not allowed in user's settings")
    return HttpResponse(status=405)


@login_required
@require_http_methods(["PUT"])
def change_password(request):
    """Method for changing password"""
    user = request.user
    id_user = request.user.id
    if request.method == 'PUT':
        put = QueryDict(request.body)
        form = ChangePasswordForm(put)
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
                    update_session_auth_hash(request, user)
                    LOGGER.debug("Successfully changed password for user %s", user)
                    return HttpResponse(status=200)
                LOGGER.warning("New password wasn't confirmed by user %s", user)
                return HttpResponse(status=400)
            LOGGER.warning("New password failed the checking")
            return HttpResponse(status=400)
        LOGGER.critical("Form for changing a password is invalid")
        return HttpResponse(status=400)
    LOGGER.critical("Other methods except PUT aren't allowed for changing a password")
    return HttpResponse(status=405)


@login_required
@require_http_methods(["DELETE"])
def delete_user(request):
    """ Method for deleting user. """
    id_user = request.user.id
    if request.method == 'DELETE':
        UserProfile.delete_user(id_user)
        logout_view(request)
        LOGGER.debug("User %s was successfully deleted", request.user)
        return HttpResponse(status=200)
    LOGGER.warning("Method isn't allowed")
    return HttpResponse(status=405)


@login_required
@require_http_methods(["PUT"])
def change_currency(request):
    """ Method for changing currencies. """
    id_user = request.user.id
    user = request.user
    if request.method == 'PUT':
        put = QueryDict(request.body)
        form = ChangeCurrencyForm(put)
        if form.is_valid():
            id_currency = int(form.cleaned_data.get('select_default_currency'))
            UserProfile.update_currency(id_currency, id_user)
            messages.success(request, 'Default currency successfully updated!')
            update_session_auth_hash(request, user)
            LOGGER.debug("Successfully changed currency for user %s", user)
            return HttpResponse(status=200)
        LOGGER.critical("Form for changing a currency is invalid")
        return HttpResponse(status=400)
    LOGGER.warning("Method isn't allowed")
    return HttpResponse(status=405)
