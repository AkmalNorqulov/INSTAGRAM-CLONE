from django.db import models
from django.conf import settings


class Reel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reels')
    video = models.FileField(upload_to='reels/videos/')
    caption = models.TextField(blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_reels', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reel {self.id} by {self.user}"

    def like_count(self):
        return self.likes.count()

    def is_liked_by(self, user):
        if not user.is_authenticated:
            return False
        return self.likes.filter(pk=user.pk).exists()
