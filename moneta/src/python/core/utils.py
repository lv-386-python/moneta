"""Module, that contain different utils (getting configs).

"""

import configparser
import logging
import os
import random
import string

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from settings.settings import DATABASES, BASE_DIR  # pylint:disable = no-name-in-module, import-error

def get_config():
    "Function for getting configs."
    conf_dict = {}
    conf = configparser.ConfigParser()
    conf.read(DATABASES['default']['OPTIONS']['read_default_file'])
    for i in conf.sections():
        conf_dict[i] = {}
        for j in conf.options(i):
            param = conf.get(i, j)
            if param.startswith('eval'):
                param = eval(param[5:-1])  # pylint:disable = eval-used
            conf_dict[i][j] = param
    return conf_dict


def get_logger(module=__name__):
    """
    Function which create an instance of logger object.
    Args:
        module: name of module
    Returns:
         logger(obj)
    """

    logging.basicConfig(
        filemode='w',
        filename=os.path.join(os.path.dirname(BASE_DIR)) + '/debug.log',
        level=logging.INFO)
    logger = logging.getLogger(module)

    return logger


def send_email(new_password, user_email):
    """Send a message to user."""
    try:
        send_mail('no reply',
                  f'Hello from "Moneta". Your new password is  {new_password}',
                  'lvmoneta386@gmail.com',
                  [user_email])
    except ValueError:
        return None
    return user_email


def random_string(stringlength=10):
    """Generate a random string of fixed length."""
    password = string.ascii_lowercase
    return ''.join(random.choice(password) for i in range(stringlength))


def hash_password(password):
    """Hash password to save it in database."""
    hashed_password = make_password(password)
    return hashed_password
