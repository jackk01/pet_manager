from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, expense_stats

router = DefaultRouter(trailing_slash=False)
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', include(router.urls)),
    path('expenses/stats', expense_stats, name='expense_stats'),
]