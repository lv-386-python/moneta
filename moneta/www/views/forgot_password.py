"""Views for resetting user password."""

from django.http import HttpResponse
from django.http.request import QueryDict
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from db.reset_password import ResetPassword
from forms.forgot_password import ResetPasswordForm


@require_http_methods(["PUT"])
def change_password_in_db(request):
    """
    View to update user password in database.
    :param request: Get request with "PUT" method and user email.
    :return: HttpResponse.
    """
    if request.method == 'PUT':
        put_data = QueryDict(request.body)
        form = ResetPasswordForm(put_data)
        if form.is_valid():
            email = put_data.get("email")
            ResetPassword.update_password(email)
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    return HttpResponse(status=400)

@require_http_methods(["GET", "POST"])
def reset_user_password(request):
    """
    View to get email from user.
    :param request: Request with information about user.
    :return: Render to forgot password template including context with list of user email.
    """
    if request.user.is_authenticated:
        return redirect('/')
    list_of_users = ResetPassword.get_list_of_user_emails()
    context = {'user_emails': list_of_users}
    return render(request, 'authentication/forgot_password.html', context)
