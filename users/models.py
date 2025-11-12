from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True, null=True)
    bio = models.TextField(max_length=250)