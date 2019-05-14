""" Views for current. """

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from db.current import Current
from forms.current import ShareCurrentForm


@login_required
@require_http_methods("POST")
def api_current_share(request, current_id, user_email):
    """
    :param request: request(obj)
    :param current_id: analysis current id(int)
    :param user_email:
    :return: html page
    """
    user = request.user
    if not Current.is_user_can_share(user, current_id):
        return HttpResponse('Permission denied', 400)
    form = ShareCurrentForm(request.POST)
    print(request.POST)
    if not form.is_valid():
        return HttpResponse('Email is not valid', 400)
    user_id = Current.is_user_valide(user_email)
    if not user_id:
        return HttpResponse(f'Share error: user({user_email}) not exist', 400)
    if Current.is_already_share_validator(current_id, user_id):
        return HttpResponse('Already shared', 200)
    Current.share(current_id, user_id)
    return HttpResponse('Successfully shared.', 200)


@login_required
@require_http_methods("DELETE")
def api_current_unshare(request, current_id, cancel_share_id):
    """
        :param request: request(obj)
        :param current_id: analysis current id(int)
        :param cancel_share_id: analysis user id(int)
        :return: html page
    """
    user = request.user
    if not Current.is_user_can_unshare(user, current_id, cancel_share_id):
        return HttpResponse('Permission denied', 400)
    Current.cancel_sharing(current_id, cancel_share_id)
    return HttpResponse(200)
