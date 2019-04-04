from django.urls import path

from ..views.expend import expend_main, expend_detailed, show_form_for_edit_expend, expend_successfully_edited


urlpatterns = [
    path('expend/', expend_main),
    path('expend/<int:expend_id>/', expend_detailed),
    path('expend/<int:expend_id>/edit/', show_form_for_edit_expend),
    path('expend/<int:expend_id>/edit/success/', expend_successfully_edited),

]
