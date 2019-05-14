"""
SETTINGS URL configuration
The `urlpatterns` list routes URLs to views.
URL for API Moneta
"""
from django.urls import path

from views.api.v1 import income

urlpatterns = [
    # INCOME URL BLOCK
    path('income/', income.api_income_list, name='create_income'),
    path('income/<int:income_id>/', income.api_income_info, name='create_income')
]
