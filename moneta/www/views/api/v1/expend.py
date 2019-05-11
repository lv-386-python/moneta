# -*- coding: utf-8 -*-

"""
Views for expend

"""
import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from core.utils import get_logger
from db.expend import Expend
from forms.expend import CreateExpendForm, EditExpendForm

# Get an instance of a LOGGER
LOGGER = get_logger(__name__)
@login_required
@require_http_methods("POST")
def api_expend_share(request, expend_id, user_email):
    """
    :param request: request(obj)
    :param expend_id: analysis current id(int)
    :param user_email:
    :return: html page
    """
    if Expend.share(expend_id, user_email):
        return HttpResponse('Successfully shared.', 200)
    return HttpResponse(f'Share error: no such user({user_email}) in database or already shared for this user.', 400)


@login_required
@require_http_methods("DELETE")
def api_expend_unshare(request, expend_id, cancel_share_id):
    """
        :param request: request(obj)
        :param expend_id: analysis current id(int)
        :param cancel_share_id: analysis user id(int)
        :return: html page
    """
    Expend.cancel_sharing(expend_id, cancel_share_id)
    return HttpResponse(200)
