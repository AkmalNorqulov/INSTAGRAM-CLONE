from django.urls import path
from .views import PostListView, PostDetailView, add_comment, toggle_like, post_create

# app_name = 'posts'
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post_create/', post_create, name='post_create'),
    path('<int:pk>/comment/', add_comment, name='add_comment'),
    path('posts/<int:pk>/like/', toggle_like, name='toggle_like'),
]