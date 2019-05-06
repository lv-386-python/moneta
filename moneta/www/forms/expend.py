"""This module provide forms for editing expend"""

from django import forms

from db.currencies import Currency
from db.storage_icon import StorageIcon


class EditExpendForm(forms.Form):
    """This class provide forms for editing expend"""
    new_name = forms.CharField(widget=forms.TextInput)
    new_amount = forms.CharField(widget=forms.NumberInput)
    new_image = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=StorageIcon.get_icon_choices_by_category("expend"),
        error_messages={"required": "You didn't select any image."})


class CreateExpendForm(forms.Form):
    '''This class provide forms for creating expend.'''
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'expend-item'}))
    currency = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'expend-item'}),
        choices=Currency.currency_list(),
        error_messages={"required": "You didn't select any currency."})
    amount = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'expend-item', 'min': '0'}))
    image = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=StorageIcon.get_icon_choices_by_category("expend"),
        error_messages={"required": "You didn't select any image."})
