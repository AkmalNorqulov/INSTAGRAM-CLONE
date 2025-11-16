from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import InstagramPost

class PostListView(ListView):
    model = InstagramPost
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']      

class PostDetailView(DetailView):
    model = InstagramPost
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

class PostCreateView(CreateView):       
    model = InstagramPost
    template_name = 'posts/post_form.html'
    fields = ['image', 'caption', 'hashtags', 'location', 'post_type']
    success_url = 'home'  
