# accounts/urls.py
from django.urls import path
from .views import register_view, ProfileView, profile_edit, notifications_list

app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('notifications/', notifications_list, name='notifications'),
]
