from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    """消费记录序列化器"""
    
    class Meta:
        model = Expense
        fields = [
            'id', 'pet', 'category', 'expense_date', 'amount', 'merchant',
            'remark', 'attachment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.attachment:
            data['attachment'] = instance.attachment.url
        else:
            data['attachment'] = None
        return data


class ExpenseCreateSerializer(serializers.ModelSerializer):
    """创建消费记录序列化器"""
    
    class Meta:
        model = Expense
        fields = [
            'pet', 'category', 'expense_date', 'amount', 'merchant', 'remark', 'attachment'
        ]