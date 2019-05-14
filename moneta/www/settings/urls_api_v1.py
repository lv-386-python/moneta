from django.urls import path

from views.api.v1 import expend, income
from views.api.v1 import image_cur

urlpatterns = [
    path('expend/create', expend.create, name='create_expend'),
    path('expend/<int:expend_id>/edit/', expend.api_edit_values),
    path('expend/', expend.api_info),

    path('images/', image_cur.get_api_images),
    path('currencies/', image_cur.get_api_currencies),

# INCOME URL BLOCK
path('income/', income.api_income_list, name='create_income'),
path('income/<int:income_id>/', income.api_income_info, name='create_income')
]
