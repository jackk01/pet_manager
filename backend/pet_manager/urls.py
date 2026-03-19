"""
URL configuration for pet_manager project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('users.urls')),
    path('api/', include('pets.urls')),
    path('api/', include('vaccinations.urls')),
    path('api/', include('health_records.urls')),
    path('api/', include('expenses.urls')),
    path('api/', include('statistics.urls')),
    path('api/', include('notifications.urls')),
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
