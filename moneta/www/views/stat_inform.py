""" Views for statistical information. """
from datetime import date, datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from core.db import responsehelper as resp
from core.utils import get_logger
from forms.stat_inform import StatisticDateForm
from src.python.db.stat_inform import Statistic

LOGGER = get_logger(__name__)


@login_required
@require_http_methods(["GET", "POST"])
def statistic_view(request):
    """
    View for a statistic.
    :param request: HTTP request
    :return: JsonResponse with data or HttpResponse
    """

    user = request.user

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StatisticDateForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            period_begin = request.POST.get("period_begin")
            period_end = request.POST.get("period_end")

            # prepare data for python datetime
            period_begin = [int(item) for item in period_begin.split('-')]
            period_end = [int(item) for item in period_end.split('-')]

            # get timestamps
            period_begin = datetime(*period_begin).timestamp()
            period_end = datetime(*period_end, 23, 59, 59).timestamp()

            statistic_data = Statistic.get_statistic_by_period(user.id, period_begin, period_end)
            data = {'statistic_data': statistic_data}
            LOGGER.debug("Return a JSON with all statictic for user %s", user)
            return JsonResponse(data, status=200)
        LOGGER.critical("Data in form %s for getting a statistic is invalid", form)
        return resp.RESPONSE_400_INVALID_DATA

    statistic_data = Statistic.get_all_statistic_by_date(user.id, date.today())
    form = StatisticDateForm()
    context = {
        'statistic_data': statistic_data,
        'form': form
    }
    LOGGER.debug("Render to a template with statistical information")
    return render(request, 'statistical_information/stat_inform.html', context)
