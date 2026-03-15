from rest_framework import serializers
from .models import HealthRecord


class HealthRecordSerializer(serializers.ModelSerializer):
    """健康记录序列化器"""
    
    class Meta:
        model = HealthRecord
        fields = [
            'id', 'pet', 'record_type', 'record_date', 'title', 'content',
            'hospital', 'doctor', 'cost', 'attachment', 'next_check_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.attachment:
            data['attachment'] = instance.attachment.url
        else:
            data['attachment'] = None
        return data


class HealthRecordCreateSerializer(serializers.ModelSerializer):
    """创建健康记录序列化器"""
    
    class Meta:
        model = HealthRecord
        fields = [
            'pet', 'record_type', 'record_date', 'title', 'content',
            'hospital', 'doctor', 'cost', 'attachment', 'next_check_date'
        ]