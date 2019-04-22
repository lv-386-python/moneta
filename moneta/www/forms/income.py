"This module provide forms for creating income"

from django import forms

from db.currencies import Currency
from db.storage_icon import StorageIcon


class AddIncomeForm(forms.Form):
    """This class provide forms for creating expend"""
    name = forms.CharField(widget=forms.TextInput)
    currency = forms.ChoiceField(
        widget=forms.Select(),
        error_messages={"required": "You didn't select any currency."},
        choices=Currency.currency_list())
    amount = forms.CharField(widget=forms.TextInput)
    image = forms.ChoiceField(widget=forms.RadioSelect(),
                              choices=StorageIcon.get_icon_choices_by_category("income"),
                              error_messages={"required": "You didn't select any image."})
