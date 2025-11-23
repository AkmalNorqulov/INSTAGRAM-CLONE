from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator # Videolarni tekshirish uchun

# Agar foydalanuvchilar mavjud bo'lsa
User = get_user_model()


# Instagram post modeli

class InstagramPost(models.Model):
    """
    Bu butun loyihaning yuragi. Rasm ham, Video (Reel) ham shu yerda saqlanadi.
    """
    
    # Post turlarini belgilaymiz
    POST_TYPE_CHOICES = (
        ('IMAGE', 'Rasm'),
        ('REEL', 'Reel (Video)'),
        ('CAROUSEL', 'Karusel'),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='instagram_posts',
        verbose_name="Muallif"
    )

    # Rasm maydoni (Video yuklanganda bo'sh qolishi mumkin -> blank=True, null=True)
    image = models.ImageField(
        upload_to='instagram_posts/images/%Y/%m/%d/',
        verbose_name="Post Rasmi",
        blank=True,
        null=True
    )

    # Video maydoni (Faqat mp4, mov, avi formatlar)
    video = models.FileField(
        upload_to='instagram_posts/videos/%Y/%m/%d/',
        verbose_name="Post Videosi",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi'])]
    )

    caption = models.TextField(max_length=2200, blank=True, verbose_name="Tavsif")
    hashtags = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)

    # Post turi: Bu maydon orqali biz Reel yoki Oddiy post ekanini ajratamiz
    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPE_CHOICES,
        default='IMAGE',
        verbose_name="Post Turi"
    )

    # Ko'rishlar soni (Reels uchun muhim)
    views_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username} - {self.post_type} ({self.pk})"

    class Meta:
        verbose_name = "Instagram Post"
        verbose_name_plural = "Instagram Postlari"
        ordering = ['-created_at']



class Comment(models.Model):
    """
    Postlarga tegishli sharhlarni ifodalovchi model.
    """
    # Qaysi postga tegishli
    post = models.ForeignKey(
        InstagramPost,
        on_delete=models.CASCADE,
        related_name='comments', # post.comments.all() orqali sharhlarga erishish uchun
        verbose_name="Post"
    )
    
    # Kim sharh qoldirgan
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Sharh Muallifi"
    )
    
    # Sharh matni
    text = models.TextField(
        max_length=500,
        verbose_name="Sharh Matni"
    )
    
    # Yaratilgan sana
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Yaratilgan Sana"
    )

    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='replies' # javoblarni olish uchun nom
    )
    
# Sharhni o'qish uchun qulay formatda qaytaradi 
    def __str__(self):
        return f"{self.author.username}: {self.text[:30]}"

# Sharh modeli uchun metama'lumotlar
    class Meta:
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"
        ordering = ['created_at'] # Eng so'nggi sharhlar birinchi ko'rinadi

# Like modeli
class Like(models.Model):
    """
    Postlarga qoldirilgan yoqtirishlarni ifodalovchi model.
    """
    post = models.ForeignKey(
        InstagramPost,
        on_delete=models.CASCADE,
        related_name='likes', # post.likes.count() orqali like soniga erishish uchun
        verbose_name="Post"
    ) # postga like qo'shish uchun
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes_given',
        verbose_name="Yoqtirgan foydalanuvchi"
    ) # user qaysi postga like bosganini ko'rsatadi
    
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Yaratilgan Sana"
    ) # yaratilgan sana ko'rsatadi

# Like modeli uchun metama'lumotlar
    class Meta:
        verbose_name = "Yoqtirish (Like)"
        verbose_name_plural = "Yoqtirishlar (Likes)"
        # Har bir foydalanuvchi bitta postga faqat bir marta like bosa olishini ta'minlaydi
        unique_together = ('post', 'user')