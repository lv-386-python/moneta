# -*- coding: utf-8 -*-

"""
Views for api expend

"""
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, QueryDict, JsonResponse
from django.views.decorators.http import require_http_methods

from core.db import responsehelper as resp
from core.utils import get_logger
from db.data_validators import ExpendValidators
from db.expend import Expend
from forms.expend import ShareExpendForm

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
    user_id = request.user.id
    info = Expend.get_expend_list_by_user_id(user_id)
    LOGGER.info("JSON was returned with all user's expends")
    return JsonResponse(info, safe=False)


@login_required
@require_http_methods(["GET"])
def api_expend_detail(request, expend_id):
    """
    API view for a single expend.
    :param request: the accepted HTTP request
    :param expend_id:
    :return: JsonResponse with data or HttpResponse
    """
    expend = Expend.get_expend_by_id(expend_id)
    if not expend:
        LOGGER.critical("Can't get an expend by id %s", expend_id)
        return resp.RESPONSE_404_OBJECT_NOT_FOUND
    LOGGER.debug("Successfully got details about expend with id %s", expend_id)
    return JsonResponse(expend, status=200)


@login_required
@require_http_methods(["GET", "PUT"])
def api_edit_values(request, expend_id):
    """
    View for interaction with edition form.
    Args:
        request (obj).
        expend_id (int) : id of expend.

    Returns:
        json response with choosen by user values.
    """
    if not Expend.can_edit(expend_id, request.user.id):
        LOGGER.warning('user %s tried to edit expend with id %s.', request.user.id, expend_id)
        raise PermissionDenied()

    if request.method == 'PUT':
        data = QueryDict(request.body)
        if ExpendValidators.data_validation(data):
            name = data['name']
            image = data['image']
            Expend.update(expend_id, name, image)
            LOGGER.info('user %s update expend %s', request.user.id, expend_id)
            return HttpResponse(200)
        LOGGER.warning(
            'User %s send invalid data on update expend with id %s.',
            request.user, expend_id)
    expend_info = Expend.get_expend_by_id(expend_id)
    currency = expend_info['currency']
    icon = expend_info['image_id']
    form = {
        'name': expend_info['name'],
        'currency': {
            'id': expend_info['currency'],
            'currency': currency},
        'amount': expend_info['amount'],
        'image': {
            'id': expend_info['image_id'],
            'css': icon}}
    LOGGER.info("Returned form for editing an expend")
    return JsonResponse(form)


@login_required
@require_http_methods(["POST"])
def create(request):
    """
    View for expend form validation and expend creation.
    Args:
        request (obj).
    """
    name = request.POST.get('name')
    id_currency = int(request.POST.get('currency'))
    amount = request.POST.get('amount')
    image = int(request.POST.get('image'))
    user = request.user.id
    data = {'status': 'create expend',
            'name': name,
            'id_currency': id_currency,
            'amount': amount,
            'image': image,
            }
    if ExpendValidators.data_validation(data):
        Expend.create_expend(name, id_currency, amount, image, user)
        expend_id = Expend.create_user_expend(user)
        LOGGER.info('User %s created new expend  with id %s.', request.user, expend_id)
        return HttpResponseRedirect('/')
    LOGGER.warning('User %s sent invalid data on creating new expend.', request.user)
    return HttpResponse('Successfully created.', 200)


@login_required
@require_http_methods("POST")
def api_expend_share(request, expend_id):
    """
    :param request: request(obj)
    :param expend_id: analysis Expend id(int)
    :return: html page
    """

    email = request.POST['email']
    form = ShareExpendForm(request.POST)
    if not form.is_valid():
        LOGGER.critical("Email isn't valid for sharing the expend")
        return HttpResponse('Email is not valid', status=400)
    user = request.user
    if not ExpendValidators.is_user_can_share(user, expend_id):
        LOGGER.warning("User didn't pass the ExpendValidators with sharing option")
        return HttpResponse('Permission denied', 400)
    user_id = ExpendValidators.is_user_valide(email, user.id)
    if not user_id:
        LOGGER.warning("Expend can not be distributed to this non-existing email ")
        return HttpResponse(f'User {email} not exist (or you want share for yourself).', status=400)
    if ExpendValidators.is_already_share_validator(expend_id, user_id):
        LOGGER.info("Expend has been already shared")
        return HttpResponse('Already shared', status=200)
    Expend.share(expend_id, user_id)
    LOGGER.info('Successfully shared the expend')
    return HttpResponse('Successfully shared.', status=200)


@login_required
@require_http_methods("DELETE")
def api_expend_unshare(request, expend_id, cancel_share_id):
    """
        :param request: request(obj)
        :param expend_id: analysis Expend id(int)
        :param cancel_share_id: analysis user id(int)
        :return: html page
    """
    if not ExpendValidators.is_unshare_id_valid(cancel_share_id):
        LOGGER.warning("Got invalid Expend's id for unsharing")
        return HttpResponse('Invalid id for unshare', status=400)
    user = request.user
    if not ExpendValidators.is_user_can_unshare(user, expend_id, cancel_share_id):
        LOGGER.warning("User %s hasn't any permission for cancel the sharing", user)
        return HttpResponse('Permission denied', status=400)
    Expend.cancel_sharing(expend_id, cancel_share_id)
    LOGGER.debug("Cancel sharing of the expend")
    return HttpResponse('Successfully unshared.', status=200)


@login_required
@require_http_methods("GET")
def api_get_expend_share_list(request, expend_id):
    """
    :param request: request(obj)
    :param expend_id: analysis expend id(int)
    :return: JSON object
    """
    user = request.user
    if not ExpendValidators.is_user_can_share(user, expend_id):
        LOGGER.warning("User %s hasn't any permission for sharing", user)
        return HttpResponse('Permission denied', 400)
    user_list = Expend.get_users_list_by_expend_id(expend_id)
    if user_list:
        data = {i: user_list[i] for i in range(len(user_list))}
    else:
        data = {}
    LOGGER.debug("Return JSON with user list by expend.id")
    return JsonResponse(data, status=200)


@login_required
@require_http_methods(["DELETE"])
def api_delete(request, expend_id):
    """
    View for expend deleting.
    :param request: the accepted HTTP request
    :param expend_id:
    :return: JsonResponse with data or HttpResponse
    """
    user_id = request.user.id
    expend = Expend.get_expend_by_id(expend_id)
    if not expend:
        LOGGER.critical("Can't find expend with id %s", expend_id)
        return resp.RESPONSE_404_OBJECT_NOT_FOUND
    Expend.delete_expend_for_user(user_id, expend_id)
    LOGGER.info('user %s deleted expend with id %s.', user_id, expend_id)
    return resp.RESPONSE_200_DELETED
