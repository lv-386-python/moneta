from django.urls import path

from current import views

app_name = 'current'

urlpatterns = [
    # ex: /current/
    path('', views.current_list, name='current_list'),
    # ex: /current/success/
    path('success/', views.current_success, name='current_success'),
    # ex: /current/5/
    path('<int:current_id>/', views.current_detail, name='current_detail'),
    # ex: /create/
    path('create/', views.current_create, name='current_create'),
    # ex: /current/5/share/
    # path('<int:current_id>/share/', views.share, name='current_share'),
    # ex: /current/5/edit/
    path('<int:current_id>/edit/', views.current_edit, name='current_edit'),
    # ex: /current/5/delete/
    path('<int:current_id>/delete/', views.current_delete, name='current_delete'),
]
