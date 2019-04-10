"Views for expend"

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from db.income import Income
from forms.add_income_form import AddIncomeForm


def create_income(request):
    "method for expend form manipulation"

    if request.method == 'POST':
        form = AddIncomeForm(request.POST)
        if form.is_valid():
            uid = request.user.id
            id_currency = int(form.cleaned_data.get('currency'))
            currency = Income.get_default_currencies()[id_currency][1]
            name = form.cleaned_data.get('name')
            amount = form.cleaned_data.get('amount')
            image_id = int(form.cleaned_data.get('image'))
            Income.create(currency=currency, name=name, amount=amount, image_id=image_id, user_id=uid)

            messages.success(request, 'New income was created')
            return HttpResponseRedirect('/')
        return HttpResponse("Invalid data")
    form = AddIncomeForm()
    # form.fields['currency'].choices = Income.get_default_currencies()
    # form.fields['image'].choices = StorageIcon.get_icon_choices_by_category("income")
    return render(request, 'income/test.html', {'form': form})
