"""
SETTINGS URL configuration
The `urlpatterns` list routes URLs to views.
URL for API Moneta
"""
from django.urls import path
from views.api.v1 import image_cur
from views.api.v1 import income, current, expend, user_settings

urlpatterns = [
    path('expend/create', expend.create, name='create_expend'),
    path('expend/<int:expend_id>/edit/', expend.api_edit_values),
    path('expend/', expend.api_info),

    path('images/', image_cur.get_api_images),
    path('currencies/', image_cur.get_api_currencies),

    # INCOME URL BLOCK
    path('income/', income.api_income_list, name='create_income'),
    path('income/<int:income_id>/', income.api_income_info, name='create_income'),
    path('current_create/', current.current_create, name='current_create'),

    # USER SETTINGS URL BLOCK
    path('user_settings/', user_settings.user_settings, name='user_profile'),
    path('change_password/', user_settings.change_password, name='user_profile'),
    path('change_currency/', user_settings.change_currency, name='change_currency'),
    path('delete_user/', user_settings.delete_user, name='delete_user'), ]
