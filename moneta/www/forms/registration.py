""" Modules for registration. """
from django import forms
from src.python.db.user_settings import UserProfile


class SignUpForm(forms.Form):
    """ Class for creating form for registration.  """
    email = forms.EmailField(max_length=254)
    select_default_currency = forms.ChoiceField(
        widget=forms.Select(),
        choices=UserProfile.get_default_currencies())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_pass = forms.CharField(widget=forms.PasswordInput())
