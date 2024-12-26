from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('new-list/', views.new_list, name='new_list'),
    path('delete-list/<int:list_id>/', views.delete_list, name='delete_list'),

    path('registro/', views.registro, name='registro'),
    path('login/', views.enter, name='login'),
    path('quit/', views.quit, name='quit'),

    path('view-list/<int:list_id>/', views.view_list, name='view_list'),

    path('view-list/<int:list_id>/send-mails/', views.send_mails, name='send_mails'),

]
