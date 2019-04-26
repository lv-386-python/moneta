""" Module with form for statistical information. """

from django import forms


class StatisticDateForm(forms.Form):
    """
    Form for statistical information.
    """

    period_begin = forms.CharField(label='Begin of period')
    period_end = forms.CharField(label='End of period')
