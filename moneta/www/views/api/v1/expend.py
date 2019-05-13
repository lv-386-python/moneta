# -*- coding: utf-8 -*-

"""
Views for expend

"""
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from core.utils import get_logger
from db.currencies import Currency
from db.expend import Expend
from db.storage_icon import StorageIcon
from forms.expend import ExpendForm
# Get an instance of a LOGGER
LOGGER = get_logger(__name__)


@login_required
@require_http_methods(["GET"])
def api_info(request):
    """
    View which returns json of all user's expends
    Args:
        request
    Returns:
        json response for api
    """
    if request.method == 'GET':
        user_id = request.user.id
        info = Expend.get_expend_list_by_user_id(user_id)
        return JsonResponse(info, safe=False)
    return HttpResponse(status=400)


@login_required
@require_http_methods(["GET", "PUT"])
def api_edit_values(request, expend_id):
    """
    View for interaction with edition form
    Args:
        request (obj).
        expend_id (int) : id of expend.

    Returns:
        json response with choosen by user values.
    """
    if not Expend.can_edit(expend_id, request.user.id):
        LOGGER.info('user %s tried to edit expend with id %s.', request.user.id, expend_id)
        raise PermissionDenied()

    if request.method == 'PUT':
        put = QueryDict(request.body)
        form = ExpendForm(put)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            amount = form.cleaned_data.get('amount')
            image = form.cleaned_data.get('image')
            Expend.update(expend_id, name, amount, image)
            LOGGER.info('user %s update expend %s', request.user.id, expend_id)
            return HttpResponse(200)
        LOGGER.error('form from user %s was invalid.', request.user.id)
        return HttpResponse(400)
    expend_info = Expend.get_expend_by_id(expend_id)
    currency = Currency.get_cur_by_id(expend_info['currency'])
    icon = StorageIcon.get_icon_by_id(expend_info['image_id'])
    form = {
        'name': expend_info['name'],
        'currency': {
            'id': expend_info['currency'],
            'currency': currency},
        'amount': expend_info['amount'],
        'image': {
            'id': expend_info['image_id'],
            'css': icon}}
    return JsonResponse(form)


@login_required
def expend_detailed(request, expend_id):
    """
    View for details of expend
    Args:
        request (obj).
        expend_id (int) : id of expend.

    Returns:
        render html page.
    """
    user_id = request.user.id

    if request.method == 'DELETE':
        if not Expend.can_edit(expend_id, request.user.id):
            raise PermissionDenied()

        Expend.delete_expend_for_user(expend_id, user_id)
        LOGGER.info('delete expend with id %s for user %s.', expend_id, user_id)
    expend = Expend.get_expend_by_id(expend_id)
    return render(
        request,
        'expend/expend_detailed.html',
        context={'expend_detailed': expend})


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    """
    View for expend form validation and expend creation.
    Args:
        request (obj).
    """
    if request.method == 'POST':
        form = ExpendForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            id_currency = int(form.cleaned_data.get('currency'))
            amount = form.cleaned_data.get('amount')
            image = int(form.cleaned_data.get('image'))
            user = request.user.id
            Expend.create_expend(name, id_currency, amount, image, user)
            expend_id = Expend.create_user_expend(user)
            LOGGER.info('User %s update expend %s.', request.user, expend_id)
            return HttpResponseRedirect('/')
        LOGGER.error('Form from user %s was invalid.', request.user.id)
        return HttpResponse("We have a problem!")


@login_required
@require_http_methods(["GET", "POST"])
def expend_share(request, expend_id):
    """
        :param request: request(obj)
        :param expend_id: analise expend id(int)
        :return: html page
    """
    if request.method == 'POST':
        Expend.share(expend_id, request.POST)
    shared_users_list = Expend.get_users_list_by_expend_id(expend_id)
    context = {'expend_list': shared_users_list}
    return render(request, "expend/expend_share.html", context)


@login_required
@require_http_methods('DELETE')
def expend_unshare(request, expend_id, cancel_share_id):
    """
        :param request: request(obj)
        :param expend_id: analysed expend id(int)
        :param cancel_share_id: analysed expend cancel_share_id(int)
        :return: html page
    """
    Expend.cancel_sharing(expend_id, cancel_share_id)
    shared_users_list = Expend.get_users_list_by_expend_id(expend_id)
    context = {'expend_list': shared_users_list}
    return render(request, "expend/expend_share.html", context)
