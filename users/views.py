from django.shortcuts import render, redirect
from django.views import View
from .models import UserProfile
from .forms import CustomUserCreationForm, CustomUserLoginForm, UserProfileUpdateForm
from django.contrib.auth import authenticate, login, logout


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        return render(request, 'users/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = CustomUserLoginForm(request)
        return render(request, 'users/login.html', {'form': form})
    def post(self, request):
        form = CustomUserLoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'users/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')

class ProfileView(View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'users/profile.html', {'profile': profile})
    
