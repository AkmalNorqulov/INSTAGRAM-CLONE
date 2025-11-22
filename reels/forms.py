from django import forms
from .models import Reel


class ReelForm(forms.ModelForm):
    class Meta:
        model = Reel
        fields = ('video', 'caption')