from django.urls import path
from . import views

app_name = 'users'
# This file defines URL patterns for the users app in a Django project.

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]