from django.shortcuts import render
from django.http import HttpResponseRedirect

from ..forms.registration_form import UserRegistrationForm
from src.python.db.registration import UserRegistration


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            def_currency = form.cleaned_data.get('def_currency')
            if not UserRegistration.user_already_exists(email):
                UserRegistration.save_user(email, password, def_currency)
                return HttpResponseRedirect('ok/')
            else:
                form = UserRegistrationForm()
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/registration.html', {'form': form})