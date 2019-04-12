# -*- coding: utf-8 -*-

"Views for expend"

import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response

from src.python.db.expend import Expend
from www.forms.expend import CreateExpendForm
from www.forms.expend import EditExpendForm


@login_required
def expend_main(request):
    "view which shows list of all user's expends"

    current_user = request.user
    if current_user.id:
        user_id = current_user.id
    else:
        user_id = 1

    expends_from_db = Expend.get_user_expends_tuple_from_db(user_id)
    if expends_from_db:
        expends_tuple = tuple(
            {
                'id': expend['id'],
                'description': f'''
                    {expend["name"]} 
                    currency:{expend["currency"]}, 
                    planned costs = {expend["amount"]} '''
            }
            for expend in expends_from_db)
    else:
        expends_tuple = (
            {
                'id': 0,
                'description': 'You have no expends',
            },
        )

    return render(
        request,
        'expend/expend_main.html',
        context={'expends_tuple': expends_tuple})


@login_required
def expend_detailed(request, expend_id=0):
    "view for details of expend"

    current_user = request.user
    if current_user.id:
        user_id = current_user.id
    else:
        user_id = 1

    if request.method == 'POST':
        if not Expend.can_edit(expend_id, request.user.id):
            raise PermissionDenied()

        Expend.delete_expend_for_user(expend_id, user_id)
        return render_to_response(
            'expend/delete.html',
            context={'user': user_id, 'expend': expend_id})

    expend = Expend.get_expend_by_id(expend_id)

    return render(
        request,
        'expend/expend_detailed.html',
        context={'expend_detailed': expend})


@login_required
def show_form_for_edit_expend(request, expend_id=1):
    "method for interaction with edit form and creation of form"
    if not Expend.can_edit(expend_id, request.user.id):
        raise PermissionDenied()

    if request.method == 'POST':
        form = EditExpendForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data.get('new_name')
            new_amount = form.cleaned_data.get('new_amount')
            new_image = form.cleaned_data.get('new_image')
            Expend.edit_name(expend_id, new_name)
            Expend.edit_amount(expend_id, new_amount)
            Expend.edit_image_id(expend_id, new_image)
            return HttpResponse(200)
        elif not form.is_valid():
            return HttpResponse(400)

    expend_info = Expend.get_expend_by_id(expend_id)

    expend_info_json = json.dumps(expend_info)
    form = EditExpendForm()
    print(expend_info_json)
    return render(
        request,
        'expend/edit_expend.html',
        context={'form': form, 'expend_info': expend_info_json})


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
