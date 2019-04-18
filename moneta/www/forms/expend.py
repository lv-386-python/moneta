'''This module provide forms for creating expend.'''
from django import forms
from src.python.db.expend import Expend
from src.python.db.storage_icon import StorageIcon


class CreateExpendForm(forms.Form):
    '''This class provide forms for creating expend.'''
    name = forms.CharField(
        widget=forms.TextInput)
    currency = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=Expend.get_default_currencies(),
        error_messages={"required": "You didn't select any currency."})
    amount = forms.CharField(
        widget=forms.TextInput)
    image = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=StorageIcon.get_icon_choices_by_category("expend"),
        error_messages={"required": "You didn't select any image."})

class ShareExpendForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput, max_length=45, label='Email')
