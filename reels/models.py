from django.db import models
from posts.models import InstagramPost  # Asosiy modelni import qilamiz

# --- CUSTOM MANAGER ---
class ReelManager(models.Manager):
    """
    Bu menejer faqat 'REEL' turidagi postlarni filtrlab beradi.
    Reel.objects.all() chaqirilganda rasm postlar aralashib ketmaydi.
    """
    def get_queryset(self):
        return super().get_queryset().filter(post_type='REEL')


# --- PROXY MODEL ---
class Reel(InstagramPost):
    """
    Reel modeli.
    
    DIQQAT: 
    1. Bu model ma'lumotlar bazasida yangi jadval YARATMAYDI (proxy=True).
    2. U 'posts_instagrampost' jadvalidagi ma'lumotlardan foydalanadi.
    3. Video, Caption, Author kabi maydonlar 'InstagramPost' dan meros olinadi.
    """
    
    # Maxsus menejerni ulaymiz
    objects = ReelManager()

    class Meta:
        proxy = True  # <--- BU ENG MUHIM QISM. Jadval yaratilmaydi.
        verbose_name = "Reel"
        verbose_name_plural = "Reels"
        # ordering = ['-created_at'] # Asosiy modeldan meros oladi

    def save(self, *args, **kwargs):
        """
        Agar shu model orqali saqlasak, 
        post_type avtomatik 'REEL' bo'lib saqlanadi.
        """
        if not self.pk:  # Agar yangi yaratilayotgan bo'lsa
            self.post_type = 'REEL'
        super().save(*args, **kwargs)