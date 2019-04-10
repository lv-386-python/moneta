""" Views for current. """

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from src.python.db.current import Current
from www.forms.current import EditCurrentForm


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


# TODO Vasyl # pylint: disable=fixme
@login_required
def current_create(request):
    """View for current creating."""
    result = Current.create_current()
    if result:
        return HttpResponse("Created")
    return HttpResponse("We have a problem!")

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
            # process the data in form.cleaned_data as required

            name = form.cleaned_data.get('name')
            image_id = form.cleaned_data.get('current_icons')
            # try to save changes to database
            result = Current.edit_current(
                current_user.id,
                current_id,
                name,
                mod_time,
                int(image_id)
            )
            # if success  - redirect to a new URL:
            if result:
                return HttpResponseRedirect(reverse('current_success'))
        else:
            context = {'current': current, 'form': form}
            return render(request, 'current/current_edit.html', context)

    # if a GET (or any other method) we'll create a blank form
    data = {'name': current['name'], 'image': current['css']}
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
        return HttpResponseRedirect(reverse('current_success'))
    context = {'current': current}
    return render(request, 'current/current_delete.html', context)

@login_required
def current_share(request, current_id):
    
    if request.method == 'POST':
        print(request.POST)
        if 'cancel_share_id' in request.POST:
            Current.cancel_sharing(current_id, request.POST['cancel_share_id'])
        if 'email' in request.POST:
            if 'can_edit' in request.POST:
                can_edit='1'
            else:
                can_edit='0'
            Current.share(current_id, request.POST['email'], can_edit)

    shared_users_list = Current.get_users_list_by_current_id(current_id)
    context = {'current_list': shared_users_list}

    return render(request, "current/current_share.html", context)  