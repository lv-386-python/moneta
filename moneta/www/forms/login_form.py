"""
This module is responsible for creating a form for logging users
"""
from django import forms
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    '''

     This is a class for creating a login form for our users
     '''

    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        """
        The clean() method on a Field subclass is responsible for running to_python(),
        validate(), and run_validators() in the correct order and propagating their errors.
        If, at any time, any of the methods raise ValidationError,
        the validation stops and that error is raised
        :return: the clean data, which is then inserted into the cleaned_data dictionary of the form
        """
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            print(type(user))
            print(user)
            if not user:
                raise forms.ValidationError('User does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
        return super(UserLoginForm, self).clean()
