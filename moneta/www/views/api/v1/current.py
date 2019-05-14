""" Views for current. """

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from db.current import Current
from db.data_validators import CurrentValidators
from forms.current import ShareCurrentForm


@login_required
@require_http_methods("POST")
def api_current_share(request, current_id):
    """
    :param request: request(obj)
    :param current_id: analysis current id(int)
    :return: html page
    """

    email = request.POST['email']
    form = ShareCurrentForm(request.POST)
    if not form.is_valid():
        return HttpResponse('Email is not valid', 400)
    user = request.user
    if not CurrentValidators.is_user_can_share(user, current_id):
        return HttpResponse('Permission denied', 400)
    user_id = CurrentValidators.is_user_valide(email)
    if not user_id:
        return HttpResponse(f'Share error: user({email}) not exist', 400)
    if CurrentValidators.is_already_share_validator(current_id, user_id):
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
    if not CurrentValidators.is_unshare_id_valid(cancel_share_id):
        return HttpResponse('Invalid id for unshare', 400)
    user = request.user
    if not CurrentValidators.is_user_can_unshare(user, current_id, cancel_share_id):
        return HttpResponse('Permission denied', 400)
    Current.cancel_sharing(current_id, cancel_share_id)
    return HttpResponse(200)
