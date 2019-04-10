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
from views.login_view import home, login_view, logout_view
import views.current as current_views

from www.views import forgot_password
from www.views.login_view import home, login_view, logout_view

urlpatterns = [

    path('', home, name='moneta-home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('not_user/', forgot_password.reset_user_password, name='no_user'),
    path('valid_email/', forgot_password.reset_user_password, name='valid_user'),
    path('forgot_password/', forgot_password.reset_user_password, name='forgot_password'),

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
    path('current/<int:current_id>/share/', current_views.current_share, name='current_share'),
    # ex: /current/5/edit/
    path('current/<int:current_id>/edit/', current_views.current_edit, name='current_edit'),
    # ex: /current/5/delete/
    path('current/<int:current_id>/delete/', current_views.current_delete, name='current_delete'),
    
]
