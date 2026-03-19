from datetime import date
from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    message_type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    days_left = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'message_type',
            'message_type_display',
            'title',
            'content',
            'pet_name',
            'due_date',
            'days_left',
            'is_read',
            'created_at',
            'updated_at',
        ]

    def get_days_left(self, obj: Notification):
        if not obj.due_date:
            return None
        return (obj.due_date - date.today()).days
