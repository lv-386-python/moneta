"Views for expend"

import json

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib import messages

from src.python.db.expend import Expend
from www.forms.expend import CreateExpendForm, EditExpendForm
from src.python.db.storage_icon import StorageIcon


def create_expend_form(request):
    "method for expend form manipulation"

    if request.method == 'POST':
        form = CreateExpendForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            currency = form.cleaned_data.get('currency')
            amount = form.cleaned_data.get('amount')
            image = form.cleaned_data.get('image')
            Expend.create_expend(name, currency, amount, image)
            messages.success(request, 'New expend was created. Congratilations!')
            return HttpesponseRedirect('expend/')
            print('B')
        else:
            print('A')
    else:
        form = CreateExpendForm()
        form.fields['currency'].choices = Expend.get_default_currencies()
        form.fields['image'].choices = StorageIcon.get_icon_choices_by_category("expend")
        return render(request, 'expend/test.html', {'form': form})


def show_form_for_edit_expend(request, expend_id=1):
    "method for interaction with edit form and creation of form"
    if request.method == 'POST':
        form = EditExpendForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data.get('new_name')
            new_planned_cost = form.cleaned_data.get('new_planned_cost')
            new_image = form.cleaned_data.get('new_image')

            Expend.edit_name(expend_id, new_name)
            Expend.edit_planned_cost(expend_id, new_planned_cost)
            Expend.edit_image_id(expend_id, new_image)

            return HttpResponseRedirect('success/')

    else:

        expend_record_from_db = Expend.get_expend_by_id(expend_id)
        expend_info = {
            'name': expend_record_from_db[1],
            'planned_cost': expend_record_from_db[5],
            'image_id': expend_record_from_db[6],
        }

        expend_info_json = json.dumps(expend_info)
        form = EditExpendForm()
        return render(
            request,
            'expend/edit_expend.html',
            context={'form': form, 'expend_info': expend_info_json})


def expend_successfully_edited(request, expend_id=0):
    "show message for successful editing"
    return render_to_response('expend/success.html')


def expend_main(request):
    "view which shows list of all user's expends"
    user_id = 1

    expends_from_db = Expend.get_user_expends_tuple_from_db(user_id)
    if expends_from_db:
        expends_tuple = tuple(
            {
                'id': expend[0],
                'description': f'{expend[1]}, currency:{expend[2]}, planned costs = {expend[-2]}'
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


def expend_detailed(request, expend_id=0):
    "view for details of expend"
    user_id = 1

    if request.method == 'POST':
        Expend.delete_expend_for_user(expend_id, user_id)
        return render_to_response(
            'expend/delete.html',
            context={'user': user_id, 'expend': expend_id})

    record_of_expend = Expend.get_expend_by_id(expend_id)
    expend = {
        'id': record_of_expend[0],
        'name': record_of_expend[1],
        'currency': record_of_expend[2],
        'planned_cost': record_of_expend[-2]
    }
    return render(
        request,
        'expend/expend_detailed.html',
        context={'expend_detailed': expend})
