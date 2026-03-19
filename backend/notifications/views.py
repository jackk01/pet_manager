from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer
from .services import sync_user_notifications


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get('days', 14))
        unread_only = request.query_params.get('unread_only', 'false').lower() == 'true'
        page = max(1, int(request.query_params.get('page', 1)))
        size = max(1, min(50, int(request.query_params.get('size', 10))))

        sync_user_notifications(request.user, days)

        queryset = Notification.objects.filter(user=request.user)
        if unread_only:
            queryset = queryset.filter(is_read=False)

        total = queryset.count()
        start = (page - 1) * size
        end = start + size
        items = queryset[start:end]

        serializer = NotificationSerializer(items, many=True)
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

        return Response({
            'items': serializer.data,
            'total': total,
            'unread_count': unread_count,
        })


class NotificationUnreadCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get('days', 14))
        sync_user_notifications(request.user, days)
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': unread_count})


class NotificationMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ids = request.data.get('ids') or []
        read_all = bool(request.data.get('read_all', False))

        queryset = Notification.objects.filter(user=request.user, is_read=False)
        if not read_all and ids:
            queryset = queryset.filter(id__in=ids)

        updated = queryset.update(is_read=True)
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

        return Response({'updated': updated, 'unread_count': unread_count})
