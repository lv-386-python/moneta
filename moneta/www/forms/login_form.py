"""
This module is responsible for creating a form for logging users
"""
from django import forms


class UserLoginForm(forms.Form):
    '''
    This is a class for creating a login form for our users
    '''
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
