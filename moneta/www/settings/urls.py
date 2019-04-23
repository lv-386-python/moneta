from django.urls import path

import views.income as income_views
import views.stat_inform as statistic
from www.views import user_settings
import views.current as current_views
from www.views import forgot_password, registration
from www.views.expend import create_expend_form
from www.views.expend import expend_main, expend_detailed, show_form_for_edit_expend
from www.views.login_view import home, login_view, logout_view

urlpatterns = [
    path('', home, name='moneta-home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('not_user/', forgot_password.reset_user_password, name='no_user'),
    path('valid_email/', forgot_password.reset_user_password, name='valid_user'),
    path('forgot_password/', forgot_password.reset_user_password, name='forgot_password'),

    path('forgot_password/', forgot_password.reset_user_password, name='forgot_password'),

    path('statistic/', statistic.statistic_view, name='statistical_information'),
    path('change_password/', user_settings.change_password, name='change_password'),
    path('delete_user/', user_settings.delete_user, name='delete_user'),
    path('change_currency/', user_settings.change_currency, name='change_currency'),
    path('user_settings/', user_settings.user_settings, name="user_settings"),
    path('registration/', registration.registration, name="registration"),

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

    path('expend/create', create_expend_form, name='create_expend'),

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
    path('income/', income_views.income_list, name='edit_income'),
    path('income/<int:income_id>/edit/', income_views.edit_income, name='edit_income'),
    path('income/<int:income_id>/delete/', income_views.delete_income, name='edit_income'),

    # Expend URLS
    path('expend/', expend_main),
    path('expend/<int:expend_id>/', expend_detailed),
    path('expend/<int:expend_id>/edit/', show_form_for_edit_expend),
]
