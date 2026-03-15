from rest_framework import serializers
from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    """宠物序列化器"""
    
    class Meta:
        model = Pet
        fields = [
            'id', 'owner', 'name', 'breed', 'gender', 'birth_date', 'weight',
            'color', 'chip_number', 'description', 'personality', 'avatar',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.avatar:
            data['avatar'] = instance.avatar.url
        else:
            data['avatar'] = None
        return data


class PetCreateSerializer(serializers.ModelSerializer):
    """创建宠物序列化器"""
    
    class Meta:
        model = Pet
        fields = [
            'name', 'breed', 'gender', 'birth_date', 'weight',
            'color', 'chip_number', 'description', 'personality', 'avatar'
        ]


class PetUpdateSerializer(serializers.ModelSerializer):
    """更新宠物序列化器"""
    
    class Meta:
        model = Pet
        fields = [
            'name', 'breed', 'gender', 'birth_date', 'weight',
            'color', 'chip_number', 'description', 'personality', 'avatar', 'is_active'
        ]