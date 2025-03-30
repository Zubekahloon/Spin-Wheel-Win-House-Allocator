from django.contrib import admin
from django.urls import path
from spinapp import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add-user/', views.add_user, name='add_user'),
    path('display-users/', views.display_users, name='display_users'),
    path('assign-house-to-user/<int:house_number>/', views.assign_house_to_user, name='assign_house_to_user'),
    path('assign_house/', views.assign_house, name='assign_house'),
]
