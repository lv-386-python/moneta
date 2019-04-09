"This module provide forms for editing expend"

from django import forms

from db.income import Income
from db.storage_icon import StorageIcon


class AddIncomeForm(forms.Form):
    "This class provide forms for creating expend"
    name = forms.CharField(widget=forms.TextInput)
    # currency = forms.ChoiceField(
    #     widget=forms.Select(choices=Income.get_default_currencies()),
    #     error_messages={"required": "You didn't select any currency."})
    currency = forms.ChoiceField(choices=Income.get_default_currencies,
                                 error_messages={"required": "You didn't select any currency."})
    amount = forms.CharField(widget=forms.TextInput)
    # image = forms.ChoiceField(widget=forms.Select(choices=StorageIcon.get_icon_choices_by_category("income")),
    #                           error_messages={"required": "You didn't select any image."})
    image = forms.ChoiceField(choices=StorageIcon.get_icon_choices_by_category("income"),
                              error_messages={"required": "You didn't select any image."})
    # def clean(self):
    #     cleaned_data = super(AddIncomeForm, self).clean()
    #     name = cleaned_data.get('name')
    #     amount = cleaned_data.get('amount')
    #     if not name and not amount:
    #         raise forms.ValidationError('You have to write something')
    #     return super(AddIncomeForm, self).clean()
