""" Module with form for statistical information. """
from datetime import date

from django import forms

from src.python.db.stat_inform import Statistic


class StatisticDateForm(forms.Form):
    """
    Form for statistical information.
    """

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id')
        super(StatisticDateForm, self).__init__(*args, **kwargs)
        self.fields['statistic_date'].widget = forms.SelectDateWidget(
            years=Statistic.get_year_list(self.user_id)
        )
        self.fields['statistic_date'].initial = date.today()

    statistic_date = forms.DateField()

    def clean(self):
        cleaned_data = super(StatisticDateForm, self).clean()
        form_date = cleaned_data.get('statistic_date')

        if form_date > date.today():
            raise forms.ValidationError('Please choose correct date. Not Future.')
        return form_date
