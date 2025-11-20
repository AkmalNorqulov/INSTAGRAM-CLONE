# Django kutubxonalar
from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django import forms

# Custom user yani admin panelda Usres yani foydalanuvchi
#  akountlarini alohida ajratib turishi uchun qilingan  clas va funksiya

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Username' 
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
    

    
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# Custom usering login formi uhcun yozilgan clas va funksiya
class CustomUserLoginForm(AuthenticationForm):
    class Meta():
        model = UserProfile
        fields = ('username', 'password')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['username'].widget.attrs['autofocus'] = True
    
    

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(self.request, username=username, password=password)

            # login qismidagi eroor uchun yozilgan fuksiya

            if user is None:
                raise forms.ValidationError(
                    "Username or password is incorrect.",
                    code="invalid_login"
                )

            
            self.user_cache = user

        return super().clean()



# Profile Update qismi uchun yozilgan class va funksiya

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['bio'].widget.attrs['placeholder'] = 'Bio'