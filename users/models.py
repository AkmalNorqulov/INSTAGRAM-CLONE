# Kodlar  uchun yozilgan django kutubxonalar

from django.db import models
from django.contrib.auth.models import AbstractUser



# Foydalanuvchi profili uchun qilinga class va funksiyalar
class UserProfile(AbstractUser):
    bio = models.TextField(max_length=300, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='profile_pictures/user.png')

    def __str__(self):
        return self.username