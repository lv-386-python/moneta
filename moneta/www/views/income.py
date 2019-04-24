"Views for income"

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from db.income import Income
from db.storage_icon import StorageIcon
from forms.income import AddIncomeForm  # pylint:disable = no-name-in-module, import-error


def create_income(request):
    """View for creating income."""
    if request.method == 'POST':
        form = AddIncomeForm(request.POST)
        if form.is_valid():
            uid = request.user.id
            oid = request.user.id
            currency = int(form.cleaned_data.get('currency'))
            name = form.cleaned_data.get('name')
            amount = int(form.cleaned_data.get('amount'))
            image_id = int(form.cleaned_data.get('image'))
            Income.create(currency=currency, name=name, amount=amount,
                          image_id=image_id, user_id=uid, owner_id=oid)
            messages.success(request, 'New income was created')
            return HttpResponse("Invalid data", status=201)
        return HttpResponse("Invalid data", status=400)
    form = AddIncomeForm()
    return render(request, 'income/add_income.html', {'form': form})


def edit_income(request, income_id):
    """View for editing income."""
    income_user = request.user
    inc_list = Income.get_income(income_user.id, income_id)
    icons = StorageIcon.get_icons("income")
    context = {'income_info': inc_list, "images": icons}
    if request.POST:
        income_name = request.POST["name"]
        income_amount = request.POST["amount"]
        income_image = request.POST["image_id"]
        Income.update_income_in_db(income_id, income_name, income_amount, income_image)
        return HttpResponse(status=200)
    return render(request, 'income/income_details.html', context)


def delete_income(request, income_id):
    """View after deleting income."""
    Income.delete_income(income_id)
    if request.POST:
        return render(request, 'income/deleted.html')
    return render(request, 'income/deleted.html')


@login_required
def income_list(request):
    """View for list of all incomes."""
    income_user = request.user
    inc_list = Income.get_income_list_by_user_id(income_user.id)
    if not inc_list:
        return render(request, 'home.html')
    context = {'income_list': inc_list}
    if request.POST:
        return render(request, 'income/edit_income.html', context)
    return render(request, 'income/edit_income.html', context)
