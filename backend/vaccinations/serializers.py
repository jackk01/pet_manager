from rest_framework import serializers
from .models import Vaccination


class VaccinationSerializer(serializers.ModelSerializer):
    """疫苗记录序列化器"""
    
    class Meta:
        model = Vaccination
        fields = [
            'id', 'pet', 'vaccine_name', 'vaccination_date', 'next_due_date',
            'clinic', 'doctor', 'batch_number', 'remark', 'attachment',
            'is_reminded', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_reminded', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.attachment:
            data['attachment'] = instance.attachment.url
        else:
            data['attachment'] = None
        return data


class VaccinationCreateSerializer(serializers.ModelSerializer):
    """创建疫苗记录序列化器"""
    
    class Meta:
        model = Vaccination
        fields = [
            'pet', 'vaccine_name', 'vaccination_date', 'next_due_date',
            'clinic', 'doctor', 'batch_number', 'remark', 'attachment'
        ]