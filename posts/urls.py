from django.urls import path
from .views import PostListView, PostDetailView, add_comment, toggle_like

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/comment/', add_comment, name='add_comment'),
    path('<int:pk>/like/', toggle_like, name='toggle_like'),
]