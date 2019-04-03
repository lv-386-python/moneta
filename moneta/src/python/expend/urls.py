from django.urls import path

import expend.views

urlpatterns = [
    path('create', expend.views.create_expend)
]
