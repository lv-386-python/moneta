""" Modules for registration. """
import jwt
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render

from core import utils
from src.python.core.db.redis_worker import RedisWorker as redis
from src.python.db.registration import Registration
from www.forms.registration import SignUpForm

ALLOWED_SAME_EMAILS_FOR_DIFFERENT_USER = 0
TOKEN_EXPIRATION_TIME_IN_REDIS = 60 * 15
TOKEN_SECRET_KEY = "SECRET_KEY"
TOKEN_ALGORITHM = 'HS256'


def registration(request):
    """ Method for users registration. """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_pass = form.cleaned_data.get('confirm_pass')
            id_currency = int(form.cleaned_data.get('select_default_currency'))
            if Registration.check_email(email) == ALLOWED_SAME_EMAILS_FOR_DIFFERENT_USER:
                if password == confirm_pass:
                    hashed_pass = utils.hash_password(password)
                    current_site = get_current_site(request)
                    domain = current_site.domain
                    is_activated = False
                    Registration.save_data(id_currency, is_activated, hashed_pass, email)
                    token = utils.token_generation(email)
                    utils.send_email_with_token(email, token, domain)
                    return render(request, 'registration/account_activation_sent.html')
                messages.error(request, "Passwords doesn't match")
            else:
                messages.error(request, "User with such email already exist")
        else:
            messages.error(request, "Form is not valid")
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_page.html', {'form': form})


def activation(request, token):
    """ Method for getting token and activating account. """
    try:
        decoded_token = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
    except jwt.DecodeError:
        return HttpResponse('Token is not valid!')

    with redis() as redis_connection:
        in_memory = redis_connection.get(token)
    email = decoded_token['email']
    id_user = Registration.get_user_id(email)
    if in_memory:
        Registration.confirm_user(id_user)
        with redis() as redis_connection:
            redis_connection.delete(token)
        message = "Email was successfully confirmed, now you can log in!"
        context = {'message': message}
        return render(request, 'registration/token_validation.html', context)
    is_activate = Registration.is_active(id_user)
    if is_activate:
        message = "User is already activated!"
        context = {'message': message}
        return render(request, 'registration/token_validation.html', context)
    current_site = get_current_site(request)
    domain = current_site.domain
    new_token = utils.token_generation(email)
    utils.send_email_with_token(email, new_token, domain)
    message = 'Your token is not valid any more. ' \
              'We have sent another token for confirmation your account to your email'
    context = {'message': message}
    return render(request, 'registration/token_validation.html', context)