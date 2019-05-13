from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

from db.currencies import Currency
from db.storage_icon import StorageIcon


@login_required
def get_api_images(request):
    if request.method == 'GET':
        return JsonResponse(StorageIcon.get_all_icons(), safe=False)
    return HttpResponse(status=400)


@login_required
def get_api_currencies(request):
    if request.method == 'GET':
        return JsonResponse(Currency.currency_list('dict'), safe=False)
    return HttpResponse(status=400)
