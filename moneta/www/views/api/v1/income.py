"""Views for income."""

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.http.request import QueryDict
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from core.utils import get_logger
from db.income import Income
from db.storage_icon import StorageIcon
from forms.income import EditIncomeForm  # pylint:disable = no-name-in-module, import-error

LOGGER = get_logger(__name__)


@require_http_methods(["POST"])
def create_income(request):
    """View for creating income."""
    uid = request.user.id
    oid = request.user.id

    currency = int(request.POST.get('currency'))
    name = request.POST.get('name')
    image_id = int(request.POST.get('image'))
    Income.create(currency=currency, name=name,
                  image_id=image_id, user_id=uid, owner_id=oid)
    LOGGER.debug("%s created the income", request.user)
    return HttpResponse("New income was created", status=201)


@require_http_methods(["PUT"])
@login_required
def edit_income(request, income_id):
    """
    View to edit income.
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
        LOGGER.debug("Form for editing an income is valid")
        return HttpResponse(status=200)
    LOGGER.warning("Form for editing an income is invalid")
    return HttpResponse(form.errors, status=400)


@require_http_methods(["DELETE"])
@login_required
def delete_income(request, income_id):
    """
    View to delete income.
    :param request: Request with DELETE method.
    :param income_id: Id of deleted income.
    :return: Response with status 200.
    """
    Income.delete_income(income_id)
    LOGGER.debug("Successfully deleted an income")
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
        LOGGER.warning("Can't get information about income of %s by id", income_user)
        return render(request, 'home.html')
    context = {'income_info': inc_list, "images": icons}
    if request.POST:
        LOGGER.debug("Render to the 'edit_income' page")
        return render(request, 'income/edit_income.html', context)
    LOGGER.debug("Render to the 'edit_income' page")
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
        income_detail = Income.get_info_income(income_user.id, income_id)
        currency = income_detail['currency']
        form = {
            'name': income_detail['name'],
            'currency': {
                'id': income_detail['currency_id'],
                'currency': currency},
            'image': {
                'id': income_detail['image_id'],
                'css': income_detail['css']}}
        LOGGER.debug("Return JSON with info about income with id %s for %s", income_id, income_user)
        return JsonResponse(form)

    if request.method == 'PUT':
        put_data = QueryDict(request.body)
        name = put_data.get("name")
        if len(name) < 45:
            image = put_data.get("image")
            mod_time = int(datetime.timestamp(datetime.now()))
            Income.update_income_in_db(income_id, name, image, mod_time)
            LOGGER.debug("Succesfully updated income with id %s in database", income_id)
            return HttpResponse(status=200)
        LOGGER.critical("Invalid data for updating an income")
        return HttpResponse("Invalid data", status=400)

    if request.method == 'DELETE':
        Income.delete_income(income_id)
        LOGGER.debug("Successfully deleted an income with id %s", income_id)
        return HttpResponse(status=200)
    LOGGER.warning("Can't delete income with id %s", income_id)
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
    LOGGER.debug("Returned JSON with information about all incomes for user %s", income_user)
    return JsonResponse(info, safe=False)
