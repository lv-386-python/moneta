"""API views for current."""

from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.http.request import QueryDict
from django.views.decorators.http import require_http_methods

from core.db import responsehelper as resp
from core.utils import get_logger
from db.currencies import Currency
from db.current import Current
from db.data_validators import CurrentValidators
from db.storage_icon import StorageIcon
from forms.current import CreateCurrentForm, EditCurrentForm, ShareCurrentForm

# Get an instance of a LOGGER
LOGGER = get_logger(__name__)

@login_required
@require_http_methods(["POST"])
def create(request):
    """
    View for current creating.
    :param request: the accepted HTTP request
    :return: JsonResponse with data or HttpResponse
    """
    if request.method == 'POST':
        form = CreateCurrentForm(request.POST)
        user_id = request.user.id
        if form.is_valid():
            name = form.cleaned_data.get('name')
            id_currency = int(form.cleaned_data.get('currency'))
            amount = form.cleaned_data.get('amount')
            image = int(form.cleaned_data.get('image'))
            owner_id = user_id
            check_current = Current.check_if_such_current_exist(owner_id, name, id_currency)
            if not check_current:
                Current.create_current(name, id_currency, amount, image, owner_id, user_id)
                LOGGER.debug("Current created succesfully")
                return HttpResponse("All is ok", status=201)
            LOGGER.warning("User %s has already created such current", owner_id)
            return HttpResponse(
                "You are already owner of current with same name and currency!", status=400)
        LOGGER.critical("Form for creation of current is invalid")
        return HttpResponse("Invalid data", status=400)
    LOGGER.critical("Request method for creation of current isn't a POST")
    return HttpResponse(status=400)


@login_required
@require_http_methods(["GET"])
def api_current_list(request):
    """
    API view for current list.
    :param request: the accepted HTTP request
    :return: JsonResponse with data or HttpResponse
    """
    current_user = request.user
    cur_list = Current.get_current_list_by_user_id(current_user.id)
    if not cur_list:
        LOGGER.warning("Can't get list of all currents for %s", current_user)
        return resp.RESPONSE_404_OBJECT_NOT_FOUND
    LOGGER.debug("Return JSON with list of all currents for user %s", current_user)
    return JsonResponse(cur_list, safe=False, status=200)


@login_required
@require_http_methods(["GET"])
def api_current_detail(request, current_id):
    """
    API view for a single current.
    :param request: the accepted HTTP request
    :param current_id:
    :return: JsonResponse with data or HttpResponse
    """
    current_user = request.user
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:
        LOGGER.error("Can't find such current %s for user %s", current_id, current_user)
        return resp.RESPONSE_404_OBJECT_NOT_FOUND
    LOGGER.info("Successfully returned JSON with the details of current %s", current)
    return JsonResponse(current, status=200)


@login_required
@require_http_methods(["GET", "PUT"])
def api_current_edit(request, current_id):
    """
    API view for current editing.
    :param request: the accepted HTTP request
    :param current_id:
    :return: JsonResponse with data or HttpResponse
    """
    current_user = request.user
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:
        return resp.RESPONSE_404_OBJECT_NOT_FOUND

    # check if user can edit a current
    if not Current.can_edit_current(current_user.id, current_id):
        LOGGER.info('user %s tried to edit current with id %s.', request.user.id, current_id)
        return resp.RESPONSE_403_ACCESS_DENIED

    if request.method == 'PUT':
        # create a form instance and populate it with data from the request:
        put_data = QueryDict(request.body)
        form = EditCurrentForm(put_data)
        # check whether it's valid:
        if form.is_valid():
            # get modification time as a timestamp
            mod_time = int(datetime.timestamp(datetime.now()))
            # get data
            name = put_data.get("name")
            image_id = int(put_data.get("image"))
            # try to save changes to database
            result = Current.edit_current(
                current_user.id, current_id, name, mod_time, image_id
            )
            if result:
                current = Current.get_current_by_id(current_user.id, current_id)
                LOGGER.info('user %s update current %s', request.user.id, current_id)
                return JsonResponse(current, status=200)
        return resp.RESPONSE_400_INVALID_DATA

    currency = Currency.get_cur_by_id(current['currency_id'])
    icon = StorageIcon.get_icon_by_id(current['image_id'])
    data_for_form = {
        'name': current['name'],
        'currency': {
            'id': current['currency'],
            'currency': currency},
        'amount': current['amount'],
        'image': {
            'id': current['image_id'],
            'css': icon}}
    return JsonResponse(data_for_form, status=200)


@login_required
@require_http_methods(["DELETE"])
def api_current_delete(request, current_id):
    """
    API view for current deleting.
    :param request: the accepted HTTP request
    :param current_id:
    :return: JsonResponse with data or HttpResponse
    """
    current_user = request.user
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:
        return resp.RESPONSE_404_OBJECT_NOT_FOUND

    Current.delete_current(current_user.id, current_id)
    LOGGER.info('user %s deleted current with id %s.', request.user.id, current_id)
    return resp.RESPONSE_200_DELETED


@login_required
@require_http_methods("POST")
def api_current_share(request, current_id):
    """
    :param request: request(obj)
    :param current_id: analysis current id(int)
    :return: HTTP status
    """

    form = ShareCurrentForm(request.POST)
    if not form.is_valid():
        return HttpResponse('Email is not valid', status=400)
    user = request.user
    if not CurrentValidators.is_user_can_share(user, current_id):
        return HttpResponse('Permission denied', status=400)
    email = request.POST['email']
    can_edit = 0
    if 'can_edit' in request.POST:
        can_edit = 1
    user_id = CurrentValidators.is_user_valide(email, user.id)
    if not user_id:
        return HttpResponse(f'User {email} not exist (or you want share for yourself).', status=400)
    if CurrentValidators.is_already_share_validator(current_id, user_id):
        return HttpResponse('Already shared', status=200)
    Current.share(current_id, user_id, can_edit)
    return HttpResponse('Successfully shared.', status=200)


@login_required
@require_http_methods("DELETE")
def api_current_unshare(request, current_id, cancel_share_id):
    """
        :param request: request(obj)
        :param current_id: analysis current id(int)
        :param cancel_share_id: analysis user id(int)
        :return: HTTP status
    """
    if not CurrentValidators.is_unshare_id_valid(cancel_share_id):
        return HttpResponse('Invalid id for unshare', status=400)
    user = request.user
    if not CurrentValidators.is_user_can_unshare(user, current_id, cancel_share_id):
        return HttpResponse('Permission denied', status=400)
    Current.cancel_sharing(current_id, cancel_share_id)
    return HttpResponse('Successfully unshared.', status=200)


@login_required
@require_http_methods("GET")
def api_get_current_share_list(request, current_id):
    """
    :param request: request(obj)
    :param current_id: analysis current id(int)
    :return: HTTP status
    """
    user = request.user
    if not CurrentValidators.is_user_can_share(user, current_id):
        return HttpResponse('Permission denied', status=400)
    user_list = Current.get_users_list_by_current_id(current_id)
    if user_list:
        data = {i: user_list[i] for i in range(len(user_list))}
    else:
        data = {}
    return JsonResponse(data, status=200)
