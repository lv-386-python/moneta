""" Modules for registration. """
from django.contrib import messages
from django.shortcuts import render
from core import utils
from src.python.db.registration import Registration
from src.python.db.user_settings import UserProfile

from ..forms.registration import SignUpForm


def registration(request):
    """ Method for users registration. """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            print(email)
            password = form.cleaned_data.get('password')
            confirm_pass = form.cleaned_data.get('confirm_pass')
            id_currency = int(form.cleaned_data.get('select_default_currency'))
            currency = UserProfile.get_default_currencies()[id_currency][1]
            if Registration.check_email(email):
                if password == confirm_pass:
                    hashed_pass = utils.hash_password(password)
                    Registration.sign_up(hashed_pass, email)
                    Registration.set_currency(currency, 1)
                    messages.success(request, "Registration is successfully, now you can log in!")
                else:
                    messages.error(request, "Passwords doesn't match")
            else:
                messages.error(request, "User with such mail already exist")
        else:
            messages.error(request, "Form is not valid")
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_page.html', {'form': form})
