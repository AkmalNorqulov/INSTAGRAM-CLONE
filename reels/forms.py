from django import forms
from django.core.exceptions import ValidationError
from .models import Reel

class ReelCreateForm(forms.ModelForm):
    """
    Yangi Reel yuklash uchun professional forma.
    """
    class Meta:
        model = Reel
        fields = ('video', 'caption')
        
        # HTML elementlariga class va atributlar qo'shish (CSS va JS uchun)
        widgets = {
            'video': forms.FileInput(attrs={
                'class': 'file-upload-input', # CSS uchun klass
                'accept': 'video/mp4,video/quicktime,video/x-m4v,video/*' # Fayl tanlash oynasida faqat videolarni ko'rsatish
            }),
            'caption': forms.Textarea(attrs={
                'class': 'caption-input',
                'rows': 4,
                'placeholder': 'Reel haqida yozing... #trend #reels',
                'maxlength': '2200'
            }),
        }

    def clean_video(self):
        """
        Video faylini qo'shimcha tekshirish (Validatsiya).
        Bu serverni katta fayllardan himoya qilish uchun kerak.
        """
        video = self.cleaned_data.get('video')
        
        if video:
            # 1. Fayl hajmini tekshirish (Limit: 100MB)
            # Agar serveringiz kuchli bo'lsa, buni oshirish mumkin.
            limit_mb = 100
            if video.size > limit_mb * 1024 * 1024:
                raise ValidationError(f"Video hajmi juda katta! Maksimal hajm: {limit_mb}MB")
            
            # 2. Fayl nomini tekshirish (Qo'shimcha xavfsizlik)
            # Modelda validator bor, lekin formada tekshirish foydalanuvchiga tezroq javob beradi.
            valid_extensions = ['.mp4', '.mov', '.avi', '.mkv']
            if not any(video.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError("Noto'g'ri format. Faqat video fayllar (MP4, MOV, AVI) yuklang.")

        return video