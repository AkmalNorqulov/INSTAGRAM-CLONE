from django.shortcuts import render, redirect
from django.views.generic import TemplateView
class HomeView(TemplateView):
    template_name = 'index.html'