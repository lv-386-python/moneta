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
from www.views.expend import (
    create_expend_form, expend_main, expend_detailed,
    show_form_for_edit_expend, expend_successfully_edited)

urlpatterns = [
    path('expend/create', create_expend_form),
    path('expend/', expend_main),
    path('expend/<int:expend_id>/', expend_detailed),
    path('expend/<int:expend_id>/edit/', show_form_for_edit_expend),
    path('expend/<int:expend_id>/edit/success/', expend_successfully_edited),
]
