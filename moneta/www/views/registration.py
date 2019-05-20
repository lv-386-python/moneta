""" Modules for registration. """
import jwt
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render

from core.utils import get_logger
from src.python.core import constants
from src.python.core import utils
from src.python.core.db.redis_worker import RedisWorker as redis
from src.python.db.registration import Registration
from www.forms.registration import SignUpForm

LOGGER = get_logger(__name__)
SECRET_KEY = constants.TOKEN_SECRET_KEY
ALGORITHM = constants.TOKEN_ALGORITHM


def registration(request):
    """ Method for users registration. """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_email_service = (email.split('@')[1])
            user_name = (email.split('@')[0])
            password = form.cleaned_data.get('password')
            confirm_pass = form.cleaned_data.get('confirm_pass')
            id_currency = int(form.cleaned_data.get('select_default_currency'))
            if not Registration.email_exist_id_db(email):
                if password == confirm_pass:
                    hashed_pass = utils.hash_password(password)
                    current_site = get_current_site(request)
                    domain = current_site.domain
                    is_activated = False
                    Registration.save_data(id_currency, is_activated, hashed_pass, email)
                    token = utils.token_generation(email)
                    utils.send_email_with_token(email, token, domain, user_name)
                    context = {"email_service": user_email_service}
                    LOGGER.debug("Render to a registration template")
                    return render(request, 'registration/account_activation_sent.html', context)
                messages.error(request, "Passwords doesn't match")
            else:
                messages.error(request, "User with such email already exist")
        else:
            messages.error(request, "Form is not valid")
    else:
        form = SignUpForm()
    LOGGER.debug("Render to a registration template")
    return render(request, 'registration/registration_page.html', {'form': form})


def activation(request, token):
    """ Method for getting token and activating account. """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.DecodeError:
        LOGGER.critical("Token for registration is invalid")
        return HttpResponse('Token is not valid!')

    with redis() as redis_connection:
        in_memory = redis_connection.get(token)
    email = decoded_token['email']
    id_user = Registration.get_user_id_by_email(email)
    if in_memory:
        Registration.confirm_user(id_user)
        with redis() as redis_connection:
            redis_connection.delete(token)
        message = "Email was successfully confirmed, now you can log in!"
        context = {'message': message}
        LOGGER.debug("Email was successfully confirmed, user %s can log in", id_user)
        return render(request, 'registration/token_validation.html', context)
    is_activate = Registration.is_active(id_user)
    if is_activate:
        message = "User is already activated!"
        context = {'message': message}
        LOGGER.info("User %s is already activated", id_user)
        return render(request, 'registration/token_validation.html', context)
    user_name = (email.split('@')[0])
    current_site = get_current_site(request)
    domain = current_site.domain
    new_token = utils.token_generation(email)
    utils.send_email_with_token(email, new_token, domain, user_name)
    message = 'Your token is not valid any more. ' \
              'We have sent another token for confirmation your account to your email'
    context = {'message': message}
    LOGGER.debug("Render to the template with token's validation")
    return render(request, 'registration/token_validation.html', context)
