# -*- coding: utf-8 -*-

"""
Views for expend

"""
import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from core.utils import get_logger
from src.python.db.expend import Expend

from www.forms.expend import CreateExpendForm
from www.forms.expend import EditExpendForm
from www.forms.expend import ShareExpendForm

# Get an instance of a LOGGER
LOGGER = get_logger(__name__)


@login_required
def expend_main(request):
    """
    View which shows list of all user's expends

    Returns:
        render html page
    """
    user_id = request.user.id

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
def expend_detailed(request, expend_id):
    """
    View for details of expend
    Args:
        request (obj).
        expend_id (int) : id of expend.

    Returns:
        render html page.
    """
    user_id = request.user.id

    if request.method == 'POST':
        if not Expend.can_edit(expend_id, request.user.id):
            raise PermissionDenied()

        Expend.delete_expend_for_user(expend_id, user_id)
        LOGGER.info('delete expend with id %s for user %s.', expend_id, user_id)
    expend = Expend.get_expend_by_id(expend_id)

    return render(
        request,
        'expend/expend_detailed.html',
        context={'expend_detailed': expend})


@login_required
def show_form_for_edit_expend(request, expend_id):
    """
    View for interaction with edition form
    Args:
        request (obj).
        expend_id (int) : id of expend.

    Returns:
        render html page.
    """
    if not Expend.can_edit(expend_id, request.user.id):
        LOGGER.info('user %s tried to edit expend with id %s.', request.user.id, expend_id)
        raise PermissionDenied()

    if request.method == 'POST':
        form = EditExpendForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data.get('new_name')
            new_amount = form.cleaned_data.get('new_amount')
            new_image = form.cleaned_data.get('new_image')
            Expend.update(expend_id, new_name, new_amount, new_image)
            LOGGER.info('user %s update expend %s', request.user.id, expend_id)
            return HttpResponse(200)
        LOGGER.error('form from user %s was invalid.', request.user.id)
        return HttpResponse(400)

    expend_info = Expend.get_expend_by_id(expend_id)
    expend_info_json = json.dumps(expend_info)
    form = EditExpendForm()

    return render(
        request,
        'expend/edit_expend.html',
        context={'form': form, 'expend_info': expend_info_json})


@login_required
def create_expend_form(request):
    """
    View for expend form manipulation.
    Args:
        request (obj).
    Returns:
        render html page.
    """
    if request.method == 'POST':
        form = CreateExpendForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            id_currency = int(form.cleaned_data.get('currency'))
            amount = form.cleaned_data.get('amount')
            image = int(form.cleaned_data.get('image'))
            user = request.user.id
            Expend.create_expend(name, id_currency, amount, image, user)
            expend_id = Expend.create_user_expend(user)
            LOGGER.info('User %s update expend %s.', request.user, expend_id)
            return HttpResponseRedirect('/')
        LOGGER.error('Form from user %s was invalid.', request.user.id)
        return HttpResponse("We have a problem!")
    form = CreateExpendForm()
    return render(request, 'expend/create_expend.html', context={'form': form})


@login_required
def expend_share(request, expend_id):
    if request.method == 'POST':
        if 'cancel_share_id' in request.POST:
            Expend.cancel_sharing(expend_id, request.POST['cancel_share_id'])
        if 'email' in request.POST:
            Expend.share(expend_id, request.POST)
    form = ShareExpendForm(request.POST)
    shared_users_list = Expend.get_users_list_by_expend_id(expend_id)
    context = {'expend_list': shared_users_list, 'form': form}

    return render(request, "expend/expend_share.html", context)  
