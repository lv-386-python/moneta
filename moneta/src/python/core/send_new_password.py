"""Module to send a new password to user."""
from django.core.mail import send_mail

def send_email(new_password, user_email):
    """Send a messsage to user."""
    try:
        send_mail('no reply',
                  f'HELLO from "Moneta"! Your new password is  {new_password}',
                  'lvmoneta386@gmail.com',
                  [user_email])
    except ValueError:
        return None