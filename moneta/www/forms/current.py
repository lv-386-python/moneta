""" Module with forms for current. """

from django import forms

from db.currencies import Currency
from db.storage_icon import StorageIcon


class CreateCurrentForm(forms.Form):
    """ This class provide forms for creating expend. """
    name = forms.CharField(
        widget=forms.TextInput)
    currency = forms.ChoiceField(
        widget=forms.Select(),
        choices=Currency.currency_list(),
        error_messages={"required": "You didn't select any currency."})
    amount = forms.CharField(
        widget=forms.TextInput)
    image = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=StorageIcon.get_icon_choices_by_category("current"),
        error_messages={"required": "You didn't select any image."})


class EditCurrentForm(forms.Form):
    """ Form for current editing. """
    name = forms.CharField(widget=forms.TextInput, max_length=45)
    amount = forms.CharField(widget=forms.NumberInput)

    current_icons = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=StorageIcon.get_icon_choices_by_category("current"),
        error_messages={"required": "You didn't select any icon."})
