""" Views for current. """

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from db.current import Current
from forms.current import CreateCurrentForm
from forms.current import EditCurrentForm


@login_required
def current_list(request):
    """View for a current list."""
    current_user = request.user
    cur_list = Current.get_current_list_by_user_id(current_user.id)
    if not cur_list:
        return HttpResponseRedirect(reverse('current_create'))
    context = {'current_list': cur_list}
    return render(request, 'current/current_list.html', context)


@login_required
def current_success(request):
    """View in a case of success request."""
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('current_list'))
    return render(request, 'current/current_success.html')


@login_required
def current_create(request):
    """View for current creating."""
    if request.method == 'POST':
        form = CreateCurrentForm(request.POST)
        user_id = request.user.id
        print(user_id)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            id_currency = int(form.cleaned_data.get('currency'))
            id_currency += 1
            amount = form.cleaned_data.get('amount')
            image = int(form.cleaned_data.get('image'))
            owner_id = user_id
            Current.create_current(name, id_currency, amount, image, owner_id, user_id)
            return HttpResponseRedirect(reverse('current_success'))
        return HttpResponse("We have a problem!")
    form = CreateCurrentForm()
    return render(request, 'current/current_create.html', context={'form': form})


@login_required
def current_detail(request, current_id):
    """View for a single current."""
    current_user = request.user
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:
        raise Http404()
    context = {'current': current}
    return render(request, 'current/current_detail.html', context)


@login_required
def current_edit(request, current_id):
    """View for editing current."""
    current_user = request.user
    # check if user can edit a current
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:
        raise Http404()
    if not Current.can_edit_current(current_user.id, current_id):
        raise PermissionDenied()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EditCurrentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # get modification time as a timestamp
            mod_time = int(datetime.timestamp(datetime.now()))

            # get data
            name = request.POST.get("name")
            amount = float(request.POST.get("amount"))
            image_id = int(request.POST.get("current_icons"))

            # try to save changes to database
            result = Current.edit_current(
                current_user.id,
                current_id,
                name,
                amount,
                mod_time,
                image_id
            )
            if result:
                current = Current.get_current_by_id(current_user.id, current_id)
                return JsonResponse(current)

        else:
            context = {'current': current, 'form': form}
            return render(request, 'current/current_edit.html', context)

    # if a GET (or any other method) we'll create a blank form
    data = {
        'name': current['name'],
        'amount': current['amount'],
        'image': current['css'],
    }

    form = EditCurrentForm(initial=data)
    context = {'current': current, 'form': form}
    return render(request, 'current/current_edit.html', context)


@login_required
def current_delete(request, current_id):
    """View for deleting current."""
    current_user = request.user
    current = Current.get_current_by_id(current_user.id, current_id)
    if not current:
        raise Http404()
    if not Current.can_edit_current(current_user.id, current_id):
        raise PermissionDenied()
    if request.method == 'POST':
        Current.delete_current(current_user.id, current_id)
        return HttpResponse(200)
    context = {'current': current}
    return render(request, 'current/current_delete.html', context)
