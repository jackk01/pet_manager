from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VaccinationViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'vaccinations', VaccinationViewSet, basename='vaccination')

urlpatterns = [
    path('', include(router.urls)),
]