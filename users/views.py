# Koddagi hamma funksiyalar uchun yozilgan kutubxonalar
from django.shortcuts import render, redirect
from django.views import View
from .models import UserProfile
from .forms import CustomUserCreationForm, CustomUserLoginForm, UserProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



# Register qismi uchun qilingan class va funksiya

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        if request.user.is_authenticated:
            return redirect('users:profile')
        return render(request, 'users/register.html', {'form': form})
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        return render(request, 'users/register.html', {'form': form})


# Login qismi uchun qilingan class va funksiya

class LoginView(View):
    def get(self, request):
        form = CustomUserLoginForm(request)
        if request.user.is_authenticated:
            return redirect('users:profile')
        return render(request, 'users/login.html', {'form': form})
    def post(self, request):
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:profile')
        return render(request, 'users/login.html', {'form': form})




# Logout qismi uchun qilingan class


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')


# Profile qismi uchun qilingan classs

class ProfileView(View):
    def get(self, request):
        profile = request.user
        return render(request, 'users/profile.html', {'profile': profile})



# Profile Update qismi uchun zilingan class va funksiya 

class ProfileUpdateView(View):
    def get(self, request):
        profile = request.user
        form = UserProfileUpdateForm(instance=profile)
        return render(request, 'users/profile_update.html', {'form': form, 'profile': profile})
    
    def post(self, request):
        profile = request.user
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        return render(request, 'users/profile_update.html', {'form': form, 'profile': profile})
    






# Settings qismi uchun qilingan classs

class SettingsView(View):
    def get(self, request):
        profile = request.user
        return render(request, 'users/settings.html', {'profile': profile})



# Search qismi uchun qilingan class

class SearchView(View):
    def get(self,request):
        profile = request.user
        return render(request, 'users/search.html', {'profile':profile})
    


# Mesagses qismi uchun qilingan class

class MesagesView(View):
    def get(self,request):
        profile = request.user
        return render(request, 'users/mesages.html', {'profile':profile})

class UserProfileView(View):
    def get(self, request, username):
        try:
            profile = UserProfile.objects.get(username=username)
            return render(request, 'users/user_profile.html', {'profile': profile})
        except UserProfile.DoesNotExist:
            message = "User not found."
            return render(request, 'users/user_profile.html', {'message': message})
        