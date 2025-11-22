from django.urls import path
from . import views


app_name = 'reels'


urlpatterns = [
path('', views.reel_list, name='list'),
path('upload/', views.reel_upload, name='upload'),
path('<int:pk>/', views.reel_detail, name='detail'),
path('<int:pk>/like-toggle/', views.reel_like_toggle, name='like-toggle'),
]