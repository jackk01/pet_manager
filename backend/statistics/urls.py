from django.urls import path
from . import views

urlpatterns = [
    path('statistics/dashboard/', views.dashboard, name='dashboard'),
    path('statistics/upcoming-vaccinations/', views.upcoming_vaccinations, name='upcoming_vaccinations'),
    path('statistics/recent-health-records/', views.recent_health_records, name='recent_health_records'),
    path('statistics/', views.expense_statistics, name='expense_statistics'),
]