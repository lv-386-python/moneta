"Views for expend"

import json

from django.contrib import messages
from django.shortcuts import render_to_response, render

from src.python.db.expend import Expend
from www.forms.expend import EditExpendForm


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
            messages.success(request, 'Expend info was updated')

    expend_info = Expend.get_expend_by_id(expend_id)

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
                'id': expend['id'],
                'description': f'''
                    {expend["name"]} 
                    currency:{expend["currency"]}, 
                    planned costs = {expend["planned_cost"]} '''
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

    expend = Expend.get_expend_by_id(expend_id)

    return render(
        request,
        'expend/expend_detailed.html',
        context={'expend_detailed': expend})
