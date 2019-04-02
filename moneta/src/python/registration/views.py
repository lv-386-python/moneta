from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import UserRegistrationForm
from .models import User

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data('email')
            def_currency = form.cleaned_data('def_currency')
            password = form.cleaned_data('password')
            User.create_user(email, def_currency,password)
            return HttpResponseRedirect('success/')
    else:
        form = UserRegistrationForm()


    return render(request, 'registration/register.html', {'form' : form})

