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
from views import login_view, forgot_password, add_income_view

urlpatterns = [
    path('', login_view.home, name='moneta-home'),
    path('login/', login_view.login_view, name='login'),
    path('logout/', login_view.logout_view, name='logout'),
    path('not_user/', forgot_password.reset_user_password, name='no_user'),
    path('valid_email/', forgot_password.reset_user_password, name='valid_user'),
    path('forgot_password/', forgot_password.reset_user_password, name='forgot_password'),
    path('add_income', add_income_view.create_income, name='add_income')
]
