# posts/urls.py
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('new/', views.new_post, name='new-post'),
    path('<slug:slug>/', views.post_detail, name='page'),
]
