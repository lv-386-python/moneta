# -*- coding: utf-8 -*-
"""api views with images and currencies
"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

from db.currencies import Currency
from db.storage_icon import StorageIcon


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
        return JsonResponse(StorageIcon.get_all_icons(), safe=False)
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
        return JsonResponse(Currency.currency_list('dict'), safe=False)
    return HttpResponse(status=400)
