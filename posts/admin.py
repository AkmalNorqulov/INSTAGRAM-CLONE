from django.contrib import admin
from .models import InstagramPost

class InstagramPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post_type', 'created_at')
    search_fields = ('caption', 'hashtags', 'location', 'author__username')
    list_filter = ('post_type', 'created_at')
    ordering = ('-created_at',)

admin.site.register(InstagramPost, InstagramPostAdmin)  