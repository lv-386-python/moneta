from django import forms


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    def_currency = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.TextInput)
