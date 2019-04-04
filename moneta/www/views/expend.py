import json

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render

from ..forms.expend import EditExpendForm
from src.python.db.expend import Expend


# from django.utils import simplejson


def show_form(request):
    "method for interaction with form and creation of form"
    if request.method == 'POST':
        form = EditExpendForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data.get('new_name')
            new_planned_cost = form.cleaned_data.get('new_planned_cost')
            new_image = form.cleaned_data.get('new_image')

            expend_id = 1
            Expend.edit_name(expend_id, new_name)
            Expend.edit_planned_cost(expend_id, new_planned_cost)
            Expend.edit_image_id(expend_id, new_image)

            return HttpResponseRedirect('success/')

    else:

        expend_record_from_db = Expend.get_expend_by_id(1)
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


def success_edit(request):
    return render_to_response('expend/success.html')


def delete_expend(request):
    # TODO view for delete expend!!!
    ''

