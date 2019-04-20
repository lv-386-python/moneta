""" Views for income. """
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from src.python.db.income import Income
from src.python.db.storage_icon import StorageIcon


def edit_income(request, income_id):
    income_user = request.user
    inc_list = Income.get_income(income_user.id, income_id)
    icons = StorageIcon.get_icons("income")
    context = {'income_info': inc_list, "images": icons}
    if request.POST:
        income_name = request.POST["name"]
        income_amount = request.POST["amount"]
        income_image = request.POST["image_id"]
        print(income_name, income_amount, income_image)
        Income.update_income_in_db(income_id, income_name, income_amount, income_image)
        return HttpResponse(status=200)
    return render(request, 'income/income_details.html', context)

def delete_income(request, income_id):
    Income.delete_income(income_id)
    print(income_id)
    if request.POST:
        return render(request, 'income/deleted.html')
    return render(request, 'income/deleted.html')

@login_required
def income_list(request):
    """View in a case of success request."""
    income_user = request.user
    inc_list = Income.get_income_list_by_user_id(income_user.id)
    context = {'income_list': inc_list}
    if request.POST:
        return render(request, 'income/edit_income.html', context)
    return render(request, 'income/edit_income.html', context)



