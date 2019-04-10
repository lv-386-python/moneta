""" Module with forms for current. """

from django import forms

from src.python.db.storage_icon import StorageIcon


class EditIncomeForm(forms.Form):
    """ Form for current editing. """
    name = forms.CharField(widget=forms.TextInput, max_length=45)

    income_icons = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=StorageIcon.get_icon_choices_by_category("income"),
        error_messages={"required": "You didn't select any icon."})
