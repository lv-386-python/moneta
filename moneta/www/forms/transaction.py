""" Module with forms for current. """

from django import forms


class TransactionForm(forms.Form):
    """ This class provide forms for creating expend. """
    id_from = forms.IntegerField(min_value=0, max_value=(10 ** 12) - 1)
    id_to = forms.IntegerField(min_value=0, max_value=(10 ** 12) - 1)
    amount_from = forms.DecimalField(min_value=0, max_value=(10 ** 12) - 1)
    amount_to = forms.DecimalField(min_value=0, max_value=(10 ** 12) - 1)
    type_from = forms.CharField(min_length=6, max_length=7)
    type_to = forms.CharField(min_length=6, max_length=7)
