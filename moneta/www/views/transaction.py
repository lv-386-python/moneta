"""
This module provides views for transaction

"""
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from core.utils import get_logger
from db.transaction_manager import make_transaction

# from django.shortcuts import render

LOGGER = get_logger(__name__)


@login_required
def transaction(request):
    """
    This view handle the transactions
    Args:
     request (obj)
    """
    user_id = request.user.id
    data = {key: val[0] for key, val in request.POST.lists()}
    data['user_id'] = user_id
    try:
        make_transaction(data)
        LOGGER.info('Transaction %s', str(data))
    except Exception:
        LOGGER.error('Transaction %s is invalid', str(data))
        return HttpResponse(400)
    return HttpResponse(200)
