from django.urls import path

from ..views.expend import show_form, success_edit


urlpatterns = [
    path('expend/edit/', show_form),
    path('expend/edit/success/', success_edit),

]
