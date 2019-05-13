"""API views for current."""

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.request import QueryDict
from django.views.decorators.http import require_http_methods

from core.db import responsehelper as resp
from db.current import Current
from forms.current import EditCurrentForm


@login_required
@require_http_methods(["GET"])
def api_current_list(request):
    """API view for current list."""
    current_user = request.user
    cur_list = Current.get_current_list_by_user_id(current_user.id)
    if not cur_list:
        return resp.RESPONSE_404_OBJECT_NOT_FOUND
    return JsonResponse(cur_list, safe=False)


@login_required
@require_http_methods(["GET"])
def api_current_detail(request, current_id):
    """API view for a single current."""
    current_user = request.user
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:
        return resp.RESPONSE_404_OBJECT_NOT_FOUND

    current_user = request.user
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:
        return resp.RESPONSE_404_OBJECT_NOT_FOUND
    return JsonResponse(current)


@login_required
@require_http_methods(["PUT"])
def api_current_edit(request, current_id):
    """API view for a current editing."""
    current_user = request.user
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:
        return resp.RESPONSE_404_OBJECT_NOT_FOUND

    # check if user can edit a current
    if not Current.can_edit_current(current_user.id, current_id):
        return resp.RESPONSE_403_ACCESS_DENIED

    # create a form instance and populate it with data from the request:
    put_data = QueryDict(request.body)
    form = EditCurrentForm(put_data)
    # check whether it's valid:
    if form.is_valid():
        # get modification time as a timestamp
        mod_time = int(datetime.timestamp(datetime.now()))
        # get data
        name = put_data.get("name")
        image_id = int(put_data.get("current_icons"))
        # try to save changes to database
        result = Current.edit_current(
            current_user.id, current_id, name, mod_time, image_id
        )
        if result:
            current = Current.get_current_by_id(current_user.id, current_id)
            return JsonResponse(current)
    return resp.RESPONSE_400_INVALID_DATA


@login_required
@require_http_methods(["DELETE"])
def api_current_delete(request, current_id):
    """API view for current deleting."""
    current_user = request.user
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:
        return resp.RESPONSE_404_OBJECT_NOT_FOUND

    Current.delete_current(current_user.id, current_id)
    return resp.RESPONSE_200_DELETED
