"""
SETTINGS URL configuration
The `urlpatterns` list routes URLs to views.
URL for API Moneta
"""
from django.urls import path

from views.api.v1 import income, current, expend

urlpatterns = [
 # INCOME URL BLOCK
               path('income/', income.api_income_list, name='create_income'),
               path('income/<int:income_id>/', income.api_income_info, name='create_income'),
 # SHARE URL BLOCK
               path('current/<int:current_id>/share/<str:user_email>', current.api_current_share, name='share_current'),
               path('current/<int:current_id>/unshare/<int:cancel_share_id>', current.api_current_unshare, name='unshare_current'),
               path('expend/<int:expend_id>/share/<str:user_email>', expend.api_expend_share, name='share_expend'),
               path('expend/<int:expend_id>/unshare/<int:cancel_share_id>', expend.api_expend_unshare, name='unshare_expend')
               ]