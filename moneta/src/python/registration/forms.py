from django import forms


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    def_currency = forms.CharField(widget=forms.TextInput)
