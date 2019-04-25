""" Modules for registration. """
from django import forms

from src.python.db.currencies import Currency


class SignUpForm(forms.Form):
    """ Class for creating form for registration.  """
    email = forms.EmailField(max_length=254)
    select_default_currency = forms.ChoiceField(
        widget=forms.Select(),
        choices=Currency.currency_list())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_pass = forms.CharField(widget=forms.PasswordInput())
