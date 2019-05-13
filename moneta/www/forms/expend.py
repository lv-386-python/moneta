"""This module provide forms for editing expend"""

from django import forms
from db.currencies import Currency
from db.storage_icon import StorageIcon


class ExpendForm(forms.Form):
    '''This class provide forms for creating expend.'''
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'expend-item', 'required': 'required'}),
        max_length=45,)
    currency = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'expend-item'}),
        choices=Currency.currency_list())
    amount = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'expend-item', 'min': '0', 'max': '1e+12'}))
    image = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"required": "required"}),
        choices=StorageIcon.get_icon_choices_by_category("expend"))
