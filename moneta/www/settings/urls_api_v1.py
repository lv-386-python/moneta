"""settings api URL Configuration
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
from views.api.v1 import income, current, expend, user_settings, image_cur, transaction

urlpatterns = [
    # INCOME URL BLOCK
    path('income/', income.api_income_list, name='create_income'),
    path('income/<int:income_id>/', income.api_income_info, name='create_income'),

    # CURRENT URL BLOCK
    path('current/create', current.create, name='create_expend'),
    path('current/', current.api_current_list, name='api_current_list'),
    path('current/<int:current_id>/', current.api_current_detail, name='api_current_detail'),
    path('current/<int:current_id>/edit/', current.api_current_edit, name='api_current_edit'),
    path('current/<int:current_id>/delete/', current.api_current_delete, name='api_current_delete'),

    # EXPEND URL BLOCK
    path('expend/create', expend.create, name='create_expend'),
    path('expend/<int:expend_id>/edit/', expend.api_edit_values),
    path('expend/', expend.api_info),

    path('images/', image_cur.get_api_images),
    path('currencies/', image_cur.get_api_currencies),

    # USER SETTINGS URL BLOCK
    path('user_settings/', user_settings.user_settings, name='user_profile'),
    path('change_password/', user_settings.change_password, name='user_profile'),
    path('change_currency/', user_settings.change_currency, name='change_currency'),
    path('delete_user/', user_settings.delete_user, name='delete_user'),

    # SHARE URL BLOCK
    path('current/<int:current_id>/share', current.api_current_share,
         name='share_current'),
    path('current/<int:current_id>/unshare/<int:cancel_share_id>', current.api_current_unshare,
         name='unshare_current'),
    path('expend/<int:expend_id>/share', expend.api_expend_share,
         name='share_expend'),
    path('expend/<int:expend_id>/unshare/<int:cancel_share_id>', expend.api_expend_unshare,
         name='unshare_expend'),
    # TRANSACTION URL BLOCK
    path('current/<int:current_id>/transaction/get', transaction.get_current_transaction,
         name='get current transactions'),
    path('income/<int:income_id>/transaction/get', transaction.get_income_transaction,
         name='get income transactions'),
    path('expend/<int:expend_id>/transaction/get', transaction.get_expend_transaction,
         name='get expend transactions'),
    path('transaction', transaction.make_transaction,
         name='make transactions'),
    path('transaction/cancel', transaction.cancel_transaction,
         name='cancel transactions'),
    ]