import json

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def update_expend(request):
    data = json.loads(request.body)
    print(data)
    print('HI')

    if True:
        return HttpResponse(status=201)
    return HttpResponse(status=400)


if __name__ == '__main__':
    pass
