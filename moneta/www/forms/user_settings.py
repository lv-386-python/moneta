""" Modules for user settings. """
from django import forms

from src.python.db.currencies import Currency

CUR_LIST = [{'', 'Default currency'}]
LIST_WITH_EMPTY = CUR_LIST + Currency.currency_list()

class ChangePasswordForm(forms.Form):
    """ Class for creating forms for changing password. """
    old_password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    new_password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    confirm_pass = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}))


class ChangeCurrencyForm(forms.Form):
    """ Class for creating forms for changing default currency. """
    select_default_currency = forms.ChoiceField(
        widget=forms.Select(),
        choices=LIST_WITH_EMPTY)
