from django.shortcuts import render
from users.models import CustomUser
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'users/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = CustomUserLoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'users/login.html', {'form': form})

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')