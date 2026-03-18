from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, ChangePasswordView, user_stats, UserSettingsView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('user/profile', UserProfileView.as_view(), name='user_profile'),
    path('user/password', ChangePasswordView.as_view(), name='change_password'),
    path('user/stats', user_stats, name='user_stats'),
    path('user/settings', UserSettingsView.as_view(), name='user_settings'),
]