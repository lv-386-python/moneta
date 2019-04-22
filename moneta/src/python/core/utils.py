"""Module, that contain different utils (getting configs).

"""

import calendar
import configparser
import logging
import os
import random
import string
from datetime import datetime

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


def get_month_range_by_date(analyzed_date):
    """
    Returns start and end of the month by date as timestamps.
    :param analyzed_date: date for handling
    :return: start and end of the month as timestamps
    """
    year = analyzed_date.year
    month = analyzed_date.month
    month_start = datetime(year, month, 1)
    month_start_timestamp = int(month_start.timestamp())
    last_day = calendar.monthrange(year, month)[1]
    month_end = datetime(year, month, last_day, 23, 59, 59)
    month_end_timestamp = int(month_end.timestamp())
    return month_start_timestamp, month_end_timestamp


def get_year_range_by_date(analyzed_date):
    """
    Returns start and end of the year by date as timestamps.
    :param analyzed_date: date for handling
    :return: start and end of the year as timestamps
    """
    year = analyzed_date.year
    year_start = datetime(year, 1, 1)
    year_start_timestamp = int(year_start.timestamp())
    # end of year - at 23:59:59 on 31 December
    year_end = datetime(year, 12, 31, 23, 59, 59)
    year_end_timestamp = int(year_end.timestamp())
    return year_start_timestamp, year_end_timestamp
