from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, ChangePasswordView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('user/password/', ChangePasswordView.as_view(), name='change_password'),
]