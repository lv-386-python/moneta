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

from views.api.v1 import income, current, expend, transaction, image_cur

urlpatterns = [
 # INCOME URL BLOCK
               path('income/', income.api_income_list, name='create_income'),
               path('income/<int:income_id>/', income.api_income_info, name='create_income'),
 # EXPEND URL BLOCK
               path('expend/create', expend.create, name='create_expend'),
               path('expend/<int:expend_id>/edit/', expend.api_edit_values),
               path('expend/', expend.api_info),

               path('images/', image_cur.get_api_images),
               path('currencies/', image_cur.get_api_currencies),
 # SHARE URL BLOCK
               path('current/<int:current_id>/share', current.api_current_share,
                    name='share_current'),
               path('current/<int:current_id>/unshare/<int:cancel_share_id>', current.api_current_unshare,
                    name='unshare_current'),
               path('expend/<int:expend_id>/share', expend.api_expend_share,
                    name='share_expend'),
               path('expend/<int:expend_id>/unshare/<int:cancel_share_id>', expend.api_expend_unshare,
                    name='unshare_expend'),
 #TRANSACTION URL BLOCK
               path('current/<int:current_id>/transaction/get', transaction.get_current_transaction,
                    name='get current transactions'),
               path('income/<int:income_id>/transaction/get', transaction.get_income_transaction,
                    name='get income transactions'),
               path('expend/<int:expend_id>/transaction/get', transaction.get_expend_transaction,
                    name='get expend transactions'),
               ]