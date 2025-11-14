from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from users.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
    
class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'bio', 'email', 'first_name', 'last_name')
