"This module provide forms for editing expend"

from django import forms


class EditExpendForm(forms.Form):
    "This class provide forms for editing expend"
    new_name = forms.CharField(widget=forms.TextInput)
    new_amount = forms.CharField(widget=forms.TextInput)
    new_image = forms.CharField(widget=forms.TextInput)
