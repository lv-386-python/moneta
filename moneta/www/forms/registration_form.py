from django import forms

CURRENCY = [
    ('usd', 'USD'),
    ('uah', 'UAH'),
    ('eur', 'EUR'),
    ('gpr', 'GPR')]

class UserRegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    def_currency = forms.CharField(label='Select default currency', widget=forms.Select(choices=CURRENCY))