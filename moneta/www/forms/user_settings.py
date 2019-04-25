""" Modules for user settings. """
from django import forms

from src.python.db.currencies import Currency


class ChangePasswordForm(forms.Form):
    """ Class for creating forms for changing password. """
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_pass = forms.CharField(widget=forms.PasswordInput())


class ChangeCurrencyForm(forms.Form):
    """ Class for creating forms for changing default currency. """
    select_default_currency = forms.ChoiceField(
        widget=forms.Select(),
        choices=Currency.currency_list())
