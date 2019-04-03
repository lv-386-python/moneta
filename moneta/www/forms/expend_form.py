from django import forms


class EditExpendForm(forms.Form):
    new_name = forms.CharField(widget=forms.TextInput)
    new_planned_cost = forms.CharField(widget=forms.TextInput)
    new_image = forms.CharField(widget=forms.TextInput)
