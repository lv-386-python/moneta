# -*- coding: utf-8 -*-
"""api views with images and currencies
"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

from core.utils import get_logger
from db.currencies import Currency
from db.storage_icon import StorageIcon

LOGGER = get_logger(__name__)


@login_required
def get_api_images(request):
    """
    View which returns json of all images
    Args:
        request
    Returns:
        json response for api
    """
    if request.method == 'GET':
        LOGGER.info("Return JSON with all images")
        return JsonResponse(StorageIcon.get_all_icons(), safe=False)
    LOGGER.error("JSON with all images wasn't returned")
    return HttpResponse(status=400)


@login_required
def get_api_currencies(request):
    """
    View which returns json of all currencies
    Args:
        request
    Returns:
        json response for api
    """
    if request.method == 'GET':
        LOGGER.info("Return JSON with all currencies")
        return JsonResponse(Currency.currency_list('dict'), safe=False)
    LOGGER.error("JSON with all currencies wasn't returned")
    return HttpResponse(status=400)
