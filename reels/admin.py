from django.contrib import admin
from .models import Reel

@admin.register(Reel)
class ReelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'like_count')
    search_fields = ('user__username', 'caption')
    readonly_fields = ('created_at',)
    