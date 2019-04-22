""" Views for statistical information. """
from datetime import date, datetime

from django.http import JsonResponse
from django.shortcuts import render

from forms.stat_inform import StatisticDateForm
from src.python.db.stat_inform import Statistic


def statistic_view(request):
    """
    View for a statistic.
    :param request: HTTP request
    :return: views for statistical information
    """

    user = request.user

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StatisticDateForm(request.POST, user_id=user.id)
        # check whether it's valid:

        if form.is_valid():
            st_year = int(request.POST.get("statistic_date_year"))
            st_month = int(request.POST.get("statistic_date_month"))
            st_day = int(request.POST.get("statistic_date_day"))
            form_date = datetime(st_year, st_month, st_day)
            statistic_data = Statistic.get_all_statistic_by_date(user.id, form_date)
            data = {'statistic_data': statistic_data}
            return JsonResponse(data)

        data = {}
        if form.non_field_errors:
            data['error_message'] = 'Please choose correct date. Not Future.'

        return JsonResponse(data)

    statistic_data = Statistic.get_all_statistic_by_date(user.id, date.today())
    form = StatisticDateForm(user_id=user.id)
    context = {
        'statistic_data': statistic_data,
        'form': form
    }
    return render(request, 'statistical_information/stat_inform.html', context)
