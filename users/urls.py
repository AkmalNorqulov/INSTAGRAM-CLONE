# Urls qismidagi url lar uchun yozilgan 
# django kutubxonalar  va claslar 


from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, ProfileUpdateView , SettingsView , SearchView , MesagesView

# Koda templateslar uchun qilingan url yo'larni
#  aniq o'sah joyga chaqirib olish uchun qilingan app name
app_name = 'users'

# Veb saytdagi saxifalar uchun qilingan url yo'lar
urlpatterns = [
    # Register qismi uchun qilingan url
    path('register/', RegisterView.as_view(), name='register'),
    # Login qismi uchun qilingan url
    path('login/', LoginView.as_view(), name='login'),
    # Profile qismi uchun qilingan url
    path('profile/', ProfileView.as_view(), name='profile'),
    # Profile update qismi uchun qilingan url
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    # Logout qismi uchun qilingan url
    path('logout/', LogoutView.as_view(), name='logout'),
    # Settings qismi uchun qilingan url
    path('settings/', SettingsView.as_view() , name='settings'),
    # Search qismi uchun qilingan url
    path('search/',SearchView.as_view(), name='search' ),
    # Mesages qismi uchun qilingan url
    path('mesages/', MesagesView.as_view(), name='mesages')

]