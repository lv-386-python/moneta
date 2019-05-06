"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from views import forgot_password, login_view, income, current, expend, stat_inform, user_settings, registration, transaction

urlpatterns = [
    path('', login_view.home, name='moneta-home'),
    path('login/', login_view.login_view, name='login'),
    path('logout/', login_view.logout_view, name='logout'),
    path('not_user/', forgot_password.reset_user_password, name='no_user'),
    path('valid_email/', forgot_password.reset_user_password, name='valid_user'),
    path('forgot_password/', forgot_password.reset_user_password, name='forgot_password'),
    path('statistic/', stat_inform.statistic_view, name='statistical_information'),
    path('change_password/', user_settings.change_password, name='change_password'),
    path('delete_user/', user_settings.delete_user, name='delete_user'),
    path('change_currency/', user_settings.change_currency, name='change_currency'),
    path('user_settings/', user_settings.user_settings, name="user_settings"),
    path('user_deleted/', user_settings.delete_user, name='user_deleted'),
    path('registration/', registration.registration, name="registration"),
    path('account_activation_sent/', registration.registration, name='account_activation_sent'),
    path('token_validation/', registration.activation, name='token_validation'),
    path('activate/<token>', registration.activation, name='activate'),
    path('add_income/', income.create_income, name='income'),
    path('forgot_password/', forgot_password.reset_user_password, name='forgot_password'),
    path('statistic/', stat_inform.statistic_view, name='statistical_information'),

    path('expend/<int:expend_id>/share/', expend.expend_share, name='expend_share'),
    # expend URL BLOCK

    # CURRENT URL BLOCK
    # ex: /current/
    path('current/', current.current_list, name='current_list'),
    # ex: /current/success/
    path('current/success/', current.current_success, name='current_success'),
    # ex: /current/5/
    path('current/<int:current_id>/', current.current_detail, name='current_detail'),
    # ex: /create/
    path('current/create/', current.current_create, name='current_create'),
    # ex: /current/5/share/
    path('current/<int:current_id>/share/', current.current_share, name='current_share'),
    # ex: /current/5/unshare/
    path('current/<int:current_id>/unshare/', current.current_unshare, name='current_unshare'),
    # ex: /current/5/edit/
    path('current/<int:current_id>/edit/', current.current_edit, name='current_edit'),
    # ex: /current/5/delete/
    path('current/<int:current_id>/delete/', current.current_delete, name='current_delete'),
    # Transactions
    path('transaction/', transaction.transaction),
    # Income
    path('income/<int:income_id>/', income.income_info, name='income_detail'),
    path('income/<int:income_id>/edit/', income.edit_income, name='edit_income'),
    path('income/<int:income_id>/delete/', income.delete_income, name='edit_income'),
    # Expend URLS
    path('expend/', expend.expend_main),
    path('expend/<int:expend_id>/', expend.expend_detailed),
    path('expend/create', expend.create_expend_form, name='create_expend'),
    path('expend/<int:expend_id>/', expend.expend_detailed, name='expend_detailed'),
    path('expend/<int:expend_id>/edit/', expend.show_form_for_edit_expend),
    path('expend/<int:expend_id>/unshare/', expend.expend_unshare, name='expend_unshare'),
]
