"Views for expend"

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from forms.add_income_form import AddIncomeForm

from db.income import Income

def create_income(request):
    "method for expend form manipulation"

    if request.method == 'POST':
        form = AddIncomeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            currency = form.cleaned_data.get('currency')
            amount = form.cleaned_data.get('amount')
            image = form.cleaned_data.get('image')
            Income.create(name, currency, amount, image)
            messages.success(request, 'New income was created')
            return HttpResponseRedirect('income/')
    else:
        form = AddIncomeForm()
    # form.fields['currency'].choices = Income.get_default_currencies()
    # form.fields['image'].choices = StorageIcon.get_icon_choices_by_category("income")
    return render(request, 'income/add_income.html', {'form': form})
