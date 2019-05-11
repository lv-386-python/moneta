""" Modules for registration. """
from django import forms

from src.python.db.currencies import Currency


class SignUpForm(forms.Form):
    """ Class for creating form for registration.  """
    email = forms.EmailField(max_length=45)
    select_default_currency = forms.ChoiceField(
        widget=forms.Select(),
        choices=Currency.currency_list())
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'class': 'reg'}))
    confirm_pass = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'class': 'reg'}))
