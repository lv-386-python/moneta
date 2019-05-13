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

from views.api.v1 import income, current

urlpatterns = [
    # INCOME URL BLOCK
    path('income/', income.api_income_list, name='create_income'),
    path('income/<int:income_id>/', income.api_income_info, name='create_income'),

    # CURRENT URL BLOCK
    path('current/', current.api_current_list, name='api_current_list'),
    path('current/<int:current_id>/', current.api_current_detail, name='api_current_detail'),
    path('current/<int:current_id>/edit/', current.api_current_edit, name='api_current_edit'),
    path('current/<int:current_id>/delete/', current.api_current_delete, name='api_current_delete'),
]
