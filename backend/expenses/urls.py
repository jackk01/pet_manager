from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, expense_stats

router = DefaultRouter(trailing_slash=False)
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('expenses/stats', expense_stats, name='expense_stats'),
    path('', include(router.urls)),
]
