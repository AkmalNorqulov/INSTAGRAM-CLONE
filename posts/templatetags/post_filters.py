# posts/templatetags/post_filters.py

from django import template

register = template.Library()

@register.filter
def split_string(value, key=','):
    """
    Berilgan matnni (value) berilgan ajratgich (key) bo'yicha ro'yxatga (list) ajratadi.
    
    Masalan: "{{ 'a,b,c'|split_string:',' }}" => ['a', 'b', 'c']
    """
    if not isinstance(value, str):
        return value
        
    return value.split(key)
    
@register.filter
def remove_spaces(value):
    """
    Matnning boshidan va oxiridan bo'sh joylarni (whitespace) olib tashlaydi.
    """
    if isinstance(value, str):
        return value.strip()
    return value





#Like
@register.simple_tag(takes_context=True)
def is_post_liked(context, post):
    """
    Berilgan postni hozirgi foydalanuvchi yoqtirganmi yoki yo'qligini tekshiradi.
    """
    request = context.get('request')
    
    # Agar foydalanuvchi tizimga kirmagan bo'lsa yoki request mavjud bo'lmasa, False qaytariladi.
    if not request or not request.user.is_authenticated:
        return False
        
    # Postning likes munosabatida hozirgi foydalanuvchini qidiramiz
    return post.likes.filter(user=request.user).exists()