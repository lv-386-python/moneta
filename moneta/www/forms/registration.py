""" Modules for registration. """
from django import forms

from src.python.db.currencies import Currency

CUR_LIST = [{'', 'Default currency'}]
LIST_WITH_EMPTY = CUR_LIST + Currency.currency_list()

class SignUpForm(forms.Form):
    """ Class for creating form for registration.  """
    email = forms.EmailField(max_length=45, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    select_default_currency = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'select_cur'}),
        choices=LIST_WITH_EMPTY,
        )
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_pass = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
