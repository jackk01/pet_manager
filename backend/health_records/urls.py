from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthRecordViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'health-records', HealthRecordViewSet, basename='health_record')

urlpatterns = [
    path('', include(router.urls)),
]