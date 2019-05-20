""" Views for current. """

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, QueryDict, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from core.utils import get_logger
from core.db import responsehelper as resp
from db.current import Current
from forms.current import EditCurrentForm, CreateCurrentForm

# Get an instance of a LOGGER
LOGGER = get_logger(__name__)


@login_required
@require_http_methods(["GET", "POST"])
def current_create(request):
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
                return HttpResponse("All is ok", status=201)
            return HttpResponse(
                "You are already owner of current with same name and currency!", status=400)
        return HttpResponse("Invalid data", status=400)
    form = CreateCurrentForm()
    return render(request, 'current/current_create.html', {'form': form})


@login_required
@require_http_methods(["GET"])
def current_detail(request, current_id):
    """
    View for a single current.
    :param request: the accepted HTTP request
    :param current_id:
    :return: JsonResponse with data or HttpResponse
    """
    current_user = request.user
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:
        return resp.RESPONSE_404_OBJECT_NOT_FOUND
    context = {'current': current, 'user_id': current_user.id}
    return render(request, 'current/current_detail.html', context)


@login_required
@require_http_methods(["GET", "PUT"])
def current_edit(request, current_id):
    """
    View for current editing.
    :param request: the accepted HTTP request
    :param current_id:
    :return: JsonResponse with data or HttpResponse
    """
    current_user = request.user
    # check if user can edit a current
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:

        return resp.RESPONSE_404_OBJECT_NOT_FOUND
    if not Current.can_edit_current(current_user.id, current_id):
        LOGGER.info('user %s tried to edit current with id %s.', request.user.id, current_id)
        return resp.RESPONSE_403_ACCESS_DENIED

    # if this is a POST request we need to process the form data
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
                return JsonResponse(current)
        else:
            context = {'current': current, 'form': form}
            return render(request, 'current/current_edit.html', context)
    # if a GET we'll create a blank form
    data = {
        'name': current['name'],
        'image': current['css'],
    }
    form = EditCurrentForm(initial=data)
    context = {'current': current, 'form': form}
    return render(request, 'current/current_edit.html', context)


@login_required
@require_http_methods(["GET", "DELETE"])
def current_delete(request, current_id):
    """
    View for current deleting.
    :param request: the accepted HTTP request
    :param current_id:
    :return: rendered page or HttpResponse
    """
    current_user = request.user
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:
        return resp.RESPONSE_404_OBJECT_NOT_FOUND
    if request.method == 'DELETE':
        Current.delete_current(current_user.id, current_id)
        LOGGER.info('user %s deleted current with id %s.', request.user.id, current_id)
        return resp.RESPONSE_200_DELETED
    context = {'current': current}
    return render(request, 'current/current_delete.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def current_share(request, current_id):
    """
        :param request: request(obj)
        :param current_id: analyzed current id(int)
        :return: html page
    """
    Current.share(current_id, request.POST)
    shared_users_list = Current.get_users_list_by_current_id(current_id)
    context = {'current_list': shared_users_list}
    return render(request, "current/current_share.html", context)


@login_required
@require_http_methods("DELETE")
def current_unshare(request, current_id, cancel_share_id):
    """
        :param request: request(obj)
        :param current_id: analyzed current id(int)
        :return: html page
    """
    if request.method == 'POST':
        Current.cancel_sharing(current_id, request.POST['cancel_share_id'])
    shared_users_list = Current.get_users_list_by_current_id(current_id)
    context = {'current_list': shared_users_list}
    return render(request, "current/current_share.html", context)


@login_required
@require_http_methods("POST")
def current_get_share_list(request, current_id):
    """
        :param request: request(obj)
        :param current_id: analyzed current id(int)
        :return: html page
    """
    Current.cancel_sharing(current_id, request.POST['cancel_share_id'])
    shared_users_list = Current.get_users_list_by_current_id(current_id)
    context = {'current_list': shared_users_list}
    return render(request, "current/current_share.html", context)
