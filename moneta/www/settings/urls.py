from django.urls import path

from www.views import forgot_password
from www.views.login_view import home, login_view, logout_view
from ..views.expend import expend_main, expend_detailed, show_form_for_edit_expend, expend_successfully_edited

urlpatterns = [
    path('expend/', expend_main),
    path('expend/<int:expend_id>/', expend_detailed),
    path('expend/<int:expend_id>/edit/', show_form_for_edit_expend),
    path('expend/<int:expend_id>/edit/success/', expend_successfully_edited),
    path('', home, name='moneta-home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('not_user/', forgot_password.reset_user_password, name='no_user'),
    path('valid_email/', forgot_password.reset_user_password, name='valid_user'),
    path('forgot_password/', forgot_password.reset_user_password, name='forgot_password')

]
