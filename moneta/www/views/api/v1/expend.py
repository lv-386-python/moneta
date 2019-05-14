""" Views for Expend. """

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from db.expend import Expend
from db.data_validators import ExpendValidators
from forms.expend import ShareExpendForm


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
        return HttpResponse('Email is not valid', 400)
    user = request.user
    if not ExpendValidators.is_user_can_share(user, expend_id):
        return HttpResponse('Permission denied', 400)
    user_id = ExpendValidators.is_user_valide(email)
    if not user_id:
        return HttpResponse(f'Share error: user({email}) not exist', 400)
    if ExpendValidators.is_already_share_validator(expend_id, user_id):
        return HttpResponse('Already shared', 200)
    Expend.share(expend_id, user_id)
    return HttpResponse('Successfully shared.', 200)


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
        return HttpResponse('Invalid id for unshare', 400)
    user = request.user
    if not ExpendValidators.is_user_can_unshare(user, expend_id, cancel_share_id):
        return HttpResponse('Permission denied', 400)
    Expend.cancel_sharing(expend_id, cancel_share_id)
    return HttpResponse(200)



