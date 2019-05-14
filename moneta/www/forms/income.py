"""This module provide forms for creating and editing income"""

from django import forms

from db.currencies import Currency
from db.storage_icon import StorageIcon


class AddIncomeForm(forms.Form):
    """This class provide forms for creating income"""
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    currency = forms.ChoiceField(
        widget=forms.Select(),
        error_messages={"required": "You didn't select any currency."},
        choices=Currency.currency_list())
    image = forms.ChoiceField(widget=forms.RadioSelect(),
                              choices=StorageIcon.get_all_icons(),
                              error_messages={"required": "You didn't select any image."})


class EditIncomeForm(forms.Form):
    """ Form for current editing. """
    name = forms.CharField(widget=forms.TextInput, max_length=45)
    income_icon = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=StorageIcon.get_all_icons(),
        error_messages={"required": "You didn't select any icon."})
