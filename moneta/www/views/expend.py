'''Views for expend.'''
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from src.python.db.expend import Expend
from www.forms.expend import CreateExpendForm


def create_expend_form(request):
    '''Method for expend form manipulation.'''
    if request.method == 'POST':
        form = CreateExpendForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            id_currency = int(form.cleaned_data.get('currency'))
            currency = Expend.get_default_currencies()[id_currency][1]
            amount = form.cleaned_data.get('amount')
            image = int(form.cleaned_data.get('image'))
            Expend.create_expend(name, currency, amount, image)
            Expend.create_user_expend(request.user.id)
            return HttpResponseRedirect('/')
        return HttpResponse("We have a problem!")
    form = CreateExpendForm()
    return render(request, 'expend/create_expend.html', context={'form': form})
