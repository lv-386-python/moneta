
""" Views for current. """

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from db.current import Current
from forms.current import CreateCurrentForm


@login_required
@require_http_methods(["POST", "GET"])
def current_create(request):
    """View for current creating."""
    if request.method == 'POST':
        form = CreateCurrentForm(request.POST)
        user_id = request.user.id
        if form.is_valid():
            name = form.cleaned_data.get('name')
            id_currency = int(form.cleaned_data.get('currency'))
            amount = form.cleaned_data.get('amount')
            image = int(form.cleaned_data.get('image'))
            owner_id = user_id
            check_current = Current.check_if_such_current_exist(owner_id, name, id_currency)
            if not check_current:
                Current.create_current(name, id_currency, amount, image, owner_id, user_id)
                return HttpResponse("All is ok", status=201)
            return HttpResponse("You are already owner of current with same name and currency!", status=400)
        return HttpResponse("Invalid data", status=400)
    return HttpResponse(status=400)


