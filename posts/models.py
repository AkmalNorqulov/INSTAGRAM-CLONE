from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Agar sizda foydalanuvchilar mavjud bo'lsa
User = get_user_model()

class InstagramPost(models.Model):
    """
    Mukammal Instagram Postini ifodalovchi model.
    """
    
    # --- Asosiy Komponentlar ---
    
    # Rasm: Postning vizual komponenti
    image = models.ImageField(
        upload_to='instagram_posts/images/',
        verbose_name="Post Rasmi"
    )

    # Sarlavha (Caption): Postning matnli qismi
    caption = models.TextField(
        max_length=2200, # Instagram cheklovi taxminan 2200 belgiga yaqin
        blank=True,
        verbose_name="Sarlavha (Caption)"
    )

    # --- Instagram-ga Xos Xususiyatlar ---
    
    # Xeshteglar: Qidiruv va tarqatish uchun
    hashtags = models.CharField(
        max_length=500, 
        blank=True,
        help_text="Xeshteglarni vergul bilan ajrating (masalan: #django, #python, #instagram)"
    )
    
    # Joylashuv: Agar post geografik joyga bog'liq bo'lsa
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Joylashuv (Location Tag)"
    )
    
    # Muallif: Postni joylashtirgan foydalanuvchi (agar ko'p foydalanuvchili bo'lsa)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='instagram_posts',
        verbose_name="Muallif"
    )

    # Post turi: Oddiy rasm, Karusel, yoki Reel
    POST_CHOICES = [
        ('IMAGE', 'Yagona Rasm'),
        ('CAROUSEL', 'Karusel'),
        ('REEL', 'Reel (Video)')
    ]
    post_type = models.CharField(
        max_length=10,
        choices=POST_CHOICES,
        default='IMAGE',
        verbose_name="Post Turi"
    )
    
    # --- Metad ma'lumotlar ---
    
    # Yaratilgan sana: Qachon yaratilgani
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Yaratilgan Sana"
    )

    # Yangilangan sana: Oxirgi marta o'zgartirilgan sana
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan Sana"
    )

    # --- Ob'ektni Ko'rsatish ---
    
    def __str__(self):
        """Ob'ektni boshqaruv panelida o'qish uchun qulay formatda qaytaradi."""
        return f"{self.author.username} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        """Model uchun metama'lumotlar."""
        verbose_name = "Instagram Posti"
        verbose_name_plural = "Instagram Postlari"
        ordering = ['-created_at'] # Eng so'nggi postlar birinchi ko'rinadi