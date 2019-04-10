""" Views for income. """

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from src.python.db.income import Income
from www.forms.income import EditIncomeForm

@login_required
def income_list(request):
    """View for a income list."""
    income_user = request.user
    inc_list = Income.get_income_list_by_user_id(income_user.id)
    print(inc_list)
    # if not inc_list:
    #     return HttpResponseRedirect(reverse('income_success'))
    context = {'income_list': inc_list}
    return render(request, 'income/income_list.html', context)

@login_required
def income_success(request):
    """View in a case of success request."""
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('income_list'))
    return render(request, 'income/income_success.html')

