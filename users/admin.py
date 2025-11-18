from django.contrib import admin
from .models import UserProfile
# Register your models here.

# Django admin paneliga kirish uchun yozilgan class

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active')