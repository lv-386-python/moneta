"""Views for resetting user password."""

from django.http import HttpResponse
from django.http.request import QueryDict
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from core.utils import get_logger
from db.reset_password import ResetPassword
from forms.forgot_password import ResetPasswordForm

LOGGER = get_logger(__name__)


@require_http_methods(["PUT"])
def change_password_in_db(request):
    """
    View to update user password in database.
    :param request: Get request with "PUT" method and user email.
    :return: HttpResponse.
    """
    put_data = QueryDict(request.body)
    form = ResetPasswordForm(put_data)
    if form.is_valid():
        email = put_data.get("email")
        ResetPassword.update_password(email)
        LOGGER.debug("Successfully changed password for user %s", request.user)
        return HttpResponse(status=200)
    LOGGER.critical("Form for changing a password for user %s is invalid", request.user)
    return HttpResponse(status=400)


@require_http_methods(["GET", "POST"])
def reset_user_password(request):
    """
    View to get email from user.
    :param request: Request with information about user.
    :return: Render to forgot password template including context with list of user email.
    """
    if request.user.is_authenticated:
        LOGGER.info("Already authenticated user %s can't reset password", request.user)
        return redirect('/')
    list_of_users = ResetPassword.get_list_of_user_emails()
    context = {'user_emails': list_of_users}
    LOGGER.debug("Render to forgot password template")
    return render(request, 'authentication/forgot_password.html', context)
