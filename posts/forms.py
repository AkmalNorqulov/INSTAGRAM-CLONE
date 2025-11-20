# posts/forms.py

from django import forms
# Sizning models.py dagi model nomingizni import qilamiz
from .models import InstagramPost 

class InstagramPostCreateForm(forms.ModelForm):
    # caption maydonini kattaroq matn maydoni (textarea) qilib belgilaymiz
    caption = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Sarlavha qo‘shish (max 2200 belgi)...'}),
        required=False
    )
    
    # post_type maydoni ModelMeta orqali avtomatik tanlanadi, lekin biz uni formaga qo'shishimiz kerak
    
    class Meta:
        model = InstagramPost
        # Muallif (author), created_at, updated_at Viewda avtomatik o'rnatiladi.
        fields = ('image', 'caption', 'hashtags', 'location', 'post_type')
        
        widgets = {
            # Faqat rasmlarni qabul qilish
            'image': forms.FileInput(attrs={'accept': 'image/*'}), 
            
            # Joylashuv uchun oddiy text input
            'location': forms.TextInput(attrs={'placeholder': 'Joylashuv qo‘shish (ixtiyoriy)'}),
            
            # Hashtaglar uchun oddiy text input
            'hashtags': forms.TextInput(attrs={'placeholder': '#tag1, #tag2, #tag3 (vergul bilan ajrating)'}),
            
            # Post turi uchun tanlov maydoni Modelda belgilangan (ChoiceField avtomatik ishlaydi)
            'post_type': forms.Select(attrs={'class': 'form-select'}), 
        }