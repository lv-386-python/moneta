"""This module provide forms for editing expend"""

from django import forms
from db.currencies import Currency
from db.storage_icon import StorageIcon


class ExpendForm(forms.Form):
    '''This class provide forms for creating expend.'''
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'expend-item', 'required': 'required'}))
    currency = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'expend-item'}),
        choices=Currency.currency_list())
    amount = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'expend-item'}))
    image = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"required": "required"}),
        choices=StorageIcon.get_all_icons())
