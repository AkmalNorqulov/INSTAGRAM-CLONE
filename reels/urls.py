from django.urls import path
from . import views

app_name = 'reels'

urlpatterns = [
    path('', views.reel_list, name='reel_list'),
    path('create/', views.reel_create, name='reel_create'),
    path('<int:pk>/', views.reel_detail, name='reel_detail'),

] 