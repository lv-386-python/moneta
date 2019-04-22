
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from src.python.db.current import Current
from src.python.db.expend import Expend


@login_required
def current_list(request):
    """View for rendering home page."""
    expend_list = Expend.get_expend_list_by_user_id(request.user.id)
    current_list = Current.get_current_list_by_user_id(request.user.id)
    context = {'current_list': current_list, 'expend_list': expend_list}
    return render(request, 'home_test.html', context)
