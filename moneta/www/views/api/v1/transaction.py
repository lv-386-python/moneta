"""
This module provides views for transaction

"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from core.utils import get_logger
from db.data_validators import TransactionValidators
from db.transaction_manager import Transaction

LOGGER = get_logger(__name__)


@login_required
@require_http_methods("GET")
def get_income_transaction(request, income_id):
    """
    This view handle the transactions
    Args:
     request (obj)
    """
    data = Transaction.get_income_transaction(income_id)
    json = {i: data[i] for i in range(len(data))}
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
    data = Transaction.get_current_transaction(current_id)
    json = {i: data[i] for i in range(len(data))}
    return JsonResponse(json, safe=False, status=200)


@login_required
@require_http_methods("GET")
def get_expend_transaction(request, expend_id):
    """
    This view handle the transactions
    Args:
     request (obj)
    """
    data = Transaction.get_expend_transaction(expend_id)
    json = {i: data[i] for i in range(len(data))}
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
    if not TransactionValidators.data_is_valid(data):
        return HttpResponse('Invalid data', status=400)
    if not TransactionValidators.can_user_make_transaction(data, user_id):
        return HttpResponse('Permission denied', status=403)
    Transaction.make_transaction(data, user_id)
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
    print(request.POST)
    for i in request.POST:
        data[i] = request.POST.get(i)
    user_id = request.user.id
    Transaction.cancel_transaction(data, user_id)
    return HttpResponse(status=200)
