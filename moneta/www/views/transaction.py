"""
This module provides views for transaction

"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from core.utils import get_logger
from db.transaction_manager import Transaction

LOGGER = get_logger(__name__)


@login_required
@require_http_methods("POST")
def transaction(request):
    """
    This view handle the transactions
    Args:
     request (obj)
    """
    user_id = request.user.id
    data = {key: val[0] for key, val in request.POST.lists()}
    data['user_id'] = user_id
    Transaction.make_transaction(data)
    LOGGER.info('Transaction %s', str(data))
    return HttpResponse(200)


@login_required
@require_http_methods("DELETE")
def cancel_transaction(request, table, transaction_id):
    """
    This view handle the transactions
    Args:
     request (obj)
    """
    user_id = request.user.id
    Transaction.make_transaction(user_id, table, transaction_id)
    LOGGER.info('Cancel transaction %s, %s', table, transaction_id)
    return HttpResponse(200)
