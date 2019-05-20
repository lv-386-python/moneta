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
    data = {key: val[0] for key, val in request.POST.lists()}
    data['user_id'] = request.user.id
    Transaction.make_transaction(data)  # pylint:disable = E1120
    LOGGER.info('Transaction %s', str(data))
    return HttpResponse(200)
