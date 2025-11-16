from django.contrib import admin
from .models import InstagramPost, Comment

class InstagramPostAdmin(admin.ModelAdmin):
    """
    InstagramPost modelini admin panelda ko'rsatish uchun admin klassi.
    """
    list_display = ('id', 'image', 'caption', 'created_at')  # Admin panelda ko'rsatiladigan ustunlar
    search_fields = ('caption',)  # Qidiruv maydoni sifatida caption ustuni
    list_filter = ('created_at',)  # Filtrlash uchun yaratilgan ustun


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created_at')
    list_filter = ('created_at', 'post')
    search_fields = ('author__username', 'text')
    date_hierarchy = 'created_at'

admin.site.register(InstagramPost, InstagramPostAdmin)