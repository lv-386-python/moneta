from django import forms

class EditExpendForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput)
    currency = forms.CharField(widget=forms.TextInput)
    image = forms.CharField(widget=forms.TextInput)
