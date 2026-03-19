from django.urls import path

from .views import NotificationListView, NotificationUnreadCountView, NotificationMarkReadView

urlpatterns = [
    path('notifications', NotificationListView.as_view(), name='notification_list'),
    path('notifications/unread-count', NotificationUnreadCountView.as_view(), name='notification_unread_count'),
    path('notifications/mark-read', NotificationMarkReadView.as_view(), name='notification_mark_read'),
]
