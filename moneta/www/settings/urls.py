from django.urls import path


from www.views import forgot_password
from www.views.login_view import home, login_view, logout_view
from www.views.expend import expend_main, expend_detailed, show_form_for_edit_expend, expend_successfully_edited
from www.views.login_view import home, login_view, logout_view
import www.views.current as current_views

from www.views import forgot_password
from www.views.login_view import home, login_view, logout_view
urlpatterns = [

    path('', home, name='moneta-home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('not_user/', forgot_password.reset_user_password, name='no_user'),
    path('valid_email/', forgot_password.reset_user_password, name='valid_user'),
    path('forgot_password/', forgot_password.reset_user_password, name='forgot_password'),
    path('forgot_password/', forgot_password.reset_user_password, name='forgot_password'),
    # CURRENT URL BLOCK
    # ex: /current/
    path('current/', current_views.current_list, name='current_list'),
    # ex: /current/success/
    path('current/success/', current_views.current_success, name='current_success'),
    # ex: /current/5/
    path('current/<int:current_id>/', current_views.current_detail, name='current_detail'),
    # ex: /create/
    path('current/create/', current_views.current_create, name='current_create'),
    # ex: /current/5/share/
    # path('<int:current_id>/share/', views.share, name='current_share'),
    # ex: /current/5/edit/
    path('current/<int:current_id>/edit/', current_views.current_edit, name='current_edit'),
    # ex: /current/5/delete/
    path('current/<int:current_id>/delete/', current_views.current_delete, name='current_delete'),

    # Expend URLS
    path('expend/', expend_main),
    path('expend/<int:expend_id>/', expend_detailed),
    path('expend/<int:expend_id>/edit/', show_form_for_edit_expend),
    path('expend/<int:expend_id>/edit/success/', expend_successfully_edited),
]
