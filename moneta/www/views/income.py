"""Views for income."""

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.http.request import QueryDict
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from db.income import Income
from db.storage_icon import StorageIcon
from forms.income import AddIncomeForm, EditIncomeForm  # pylint:disable = no-name-in-module, import-error


@require_http_methods(["GET", "POST"])
def create_income(request):
    """View for creating income."""
    if request.method == 'POST':
        form = AddIncomeForm(request.POST)
        if form.is_valid():
            currency = int(form.cleaned_data.get('currency'))
            name = form.cleaned_data.get('name')
            image_id = int(form.cleaned_data.get('image'))
            Income.create(currency=currency, name=name, image_id=image_id, user_id=request.user.id,
                          owner_id=request.user.id)
            messages.success(request, 'New income was created')
            return HttpResponse("Success", status=201)
        return HttpResponse("Invalid data", status=400)
    form = AddIncomeForm()
    return render(request, 'income/add_income.html', {'form': form})


@require_http_methods(["PUT"])
@login_required
def edit_income(request, income_id):
    """
    View for editing income.
    :param request: Request with PUT method that get a dict with  name and image_id.
    :param income_id: Id of editted income.
    :return: Response with status 200.
    """
    put_data = QueryDict(request.body)
    form = EditIncomeForm(put_data)
    if form.is_valid():
        name = put_data.get("name")
        image = put_data.get("income_icon")
        mod_time = int(datetime.timestamp(datetime.now()))
        Income.update_income_in_db(income_id, name, image, mod_time)
        return HttpResponse(status=200)
    return HttpResponse(form.errors, status=400)


@require_http_methods(["DELETE"])
@login_required
def delete_income(request, income_id):
    """
    View for deletting income.
    :param request: Request with DELETE method.
    :param income_id: Id of deletted income.
    :return: Response with status 200.
    """
    Income.delete_income(income_id)
    return HttpResponse(status=200)


@require_http_methods(["GET", "POST"])
@login_required
def income_info(request, income_id):
    """
    View for detailed information about income by id.
    :param request: Request with GET or POST method.
    :param income_id: Id of income.
    :return: Render to template including context with information about it and list of icons.
    """
    income_user = request.user
    inc_list = Income.get_info_income(income_user.id, income_id)
    icons = StorageIcon.get_all_icons()
    if not inc_list:
        return render(request, 'home.html')
    context = {'income_info': inc_list, "images": icons}
    if request.POST:
        return render(request, 'income/edit_income.html', context)
    return render(request, 'income/edit_income.html', context)


@require_http_methods(["GET", "PUT", "DELETE"])
@login_required
def api_income_info(request, income_id):
    """
    View for api with detailed information about income by id.
    :param request: Request with GET method.
    :param income_id: Id of income.
    :return: JsonResponse with information about income.
    """
    if request.method == "GET":
        income_user = request.user
        info = Income.get_info_income(income_user.id, income_id)
        if info:
            return JsonResponse(info, safe=False, status=200)
        return HttpResponse(status=400)
    if request.method == 'PUT':
        put_data = QueryDict(request.body)
        form = EditIncomeForm(put_data)
        if form.is_valid():
            name = put_data.get("name")
            image = put_data.get("income_icon")
            mod_time = int(datetime.timestamp(datetime.now()))
            Income.update_income_in_db(income_id, name, image, mod_time)
            return HttpResponse(status=200)
        return HttpResponse(form.errors, status=400)
    if request.method == 'DELETE':
        Income.delete_income(income_id)
        return HttpResponse(status=200)
    return HttpResponse(status=400)


@require_http_methods(["GET"])
@login_required
def api_income_list(request):
    """
    View for api with detailed information about all incomes.
    :param request: Request with GET method.
    :return: JsonResponse with information about all incomes.
    """
    income_user = request.user
    info = Income.get_income_list_by_user_id(income_user.id)
    return JsonResponse(info, safe=False)
    