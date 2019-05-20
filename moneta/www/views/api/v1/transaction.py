"""
This module provides views for transaction

"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from core.utils import get_logger
from db.data_validators import TransactionValidators
from db.transaction_manager import Transaction
from forms.transaction import TransactionForm

LOGGER = get_logger(__name__)


@login_required
@require_http_methods("GET")
def get_income_transaction(request, income_id):
    """
    This view handle the transactions
    Args:
     request (obj)
     income_id
    """
    user = request.user.id
    if not TransactionValidators.can_get_income_transaction(user, income_id):
        LOGGER.warning("Denied permission for create a transaction from income with id {income_id} "
                       "for user {user} ".format(user=user, income_id=income_id))
        return HttpResponse('Permission denied', status=403)
    data = Transaction.get_income_transaction(income_id)
    json = {i: data[i] for i in range(len(data))}
    LOGGER.debug("Succesfully make transaction from income with id {income_id} "
                 "by user {user}".format(income_id=income_id, user=user))
    return JsonResponse(json, safe=False, status=200)


@login_required
@require_http_methods("GET")
def get_current_transaction(request, current_id):
    """
    This view handle the transactions
    Args:
     request (obj)
     current_id
    """
    user = request.user.id
    if not TransactionValidators.can_get_current_transaction(user, current_id):
        LOGGER.warning("Denied permission for create a transaction from income with id {current_id} "
                       "for user {user} ".format(user=user, current_id=current_id))
        return HttpResponse('Permission denied', status=403)
    data = Transaction.get_current_transaction(current_id)
    json = {i: data[i] for i in range(len(data))}
    LOGGER.debug("Succesfully make transaction from current with id {current_id} "
                 "by user {user}".format(current_id=current_id, user=user))
    return JsonResponse(json, safe=False, status=200)


@login_required
@require_http_methods("GET")
def get_expend_transaction(request, expend_id):
    """
    This view handle the transactions
    Args:
     request (obj)
    """
    user = request.user.id
    if not TransactionValidators.can_get_expend_transaction(user, expend_id):
        LOGGER.warning("Denied permission for create a transaction from income with id {expend_id} "
                       "for user {user} ".format(user=user, expend_id=expend_id))
        return HttpResponse('Permission denied', status=403)
    data = Transaction.get_expend_transaction(expend_id)
    json = {i: data[i] for i in range(len(data))}
    LOGGER.debug("Succesfully make transaction from current with id {expend_id} "
                 "by user {user}".format(expend_id=expend_id, user=user))
    return JsonResponse(json, safe=False, status=200)


@login_required
@require_http_methods("POST")
def make_transaction(request):
    """
    This view handle the transactions
    Args:
     request (obj)
    """
    data = {}
    for i in request.POST:
        data[i] = request.POST.get(i)
    user_id = request.user.id
    form = TransactionForm(request.POST)
    if not form.is_valid():
        LOGGER.warning("Data {} hasn't passed the validation".format(form))
        return HttpResponse('Invalid form data', status=400)
    if not TransactionValidators.data_is_valid(data):
        LOGGER.warning("Data {} hasn't passed the validation in TransactionValidators".format(form))
        return HttpResponse('Invalid data', status=400)
    if not TransactionValidators.can_user_make_transaction(data, user_id):
        LOGGER.warning("User {} doesn't have a permission for making a transaction".format(user_id))
        return HttpResponse('Permission denied', status=403)
    Transaction.make_transaction(data, user_id)
    LOGGER.debug("User {} successfully maked a transaction".format(user_id))
    return HttpResponse(status=200)


@login_required
@require_http_methods("POST")
def cancel_transaction(request):
    """
    This view handle the transactions
    Args:
     request (obj)
    """
    data = {}
    for i in request.POST:
        data[i] = request.POST.get(i)
    user_id = request.user.id
    Transaction.cancel_transaction(data, user_id)
    LOGGER.debug("Successfully canceled the transaction by user {}".format(user_id))
    return HttpResponse(status=200)
