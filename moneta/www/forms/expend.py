"This module provide forms for editing expend"

from django import forms


class CreateExpendForm(forms.Form):
    "This class provide forms for creating expend"
    name = forms.CharField(widget=forms.TextInput)
    currency = forms.ChoiceField(
        widget=forms.CheckboxInput,
        error_messages={"required": "You didn't select any currency."})
    amount = forms.CharField(widget=forms.TextInput)
    image_id = forms.CharField(widget=forms.TextInput)
    image = forms.ChoiceField(
        widget=forms.RadioSelect,
        error_messages={"required": "You didn't select any image."})


class EditExpendForm(forms.Form):
    "This class provide forms for editing expend"
    new_name = forms.CharField(widget=forms.TextInput)
    new_planned_cost = forms.CharField(widget=forms.TextInput)
    new_image = forms.CharField(widget=forms.TextInput)
