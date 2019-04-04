from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import UserRegistrationForm
from .models import UserRegistration


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            def_currency = form.cleaned_data.get('def_currency')
            if email == UserRegistration.already_exists_user(email):
                return HttpResponseRedirect('registration/register.html')
            UserRegistration.save_user(email, password, def_currency)
            return HttpResponseRedirect('ok/')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
