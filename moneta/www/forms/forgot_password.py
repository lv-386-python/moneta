"""  This module provide form for resetting password. """

from django import forms


class ResetPasswordForm(forms.Form):
    """ Class for creating form for registration.  """
    email = forms.EmailField(max_length=45)
    