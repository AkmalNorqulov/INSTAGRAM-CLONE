from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView 

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'), 
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
]   