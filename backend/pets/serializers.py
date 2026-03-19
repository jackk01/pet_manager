import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Pet


class Base64ImageField(serializers.ImageField):
    """支持 base64 格式图片的字段"""

    def to_internal_value(self, data):
        # 处理空值
        if data is None or data == '' or data == 'null' or data == 'undefined':
            return None

        if isinstance(data, str) and data.startswith('data:image'):
            # 解析 base64 数据
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            # 生成唯一文件名
            filename = f"{uuid.uuid4().hex}.{ext}"
            data = ContentFile(base64.b64decode(imgstr), name=filename)
        elif isinstance(data, str):
            # 非 base64 格式的字符串，返回 None
            return None

        return super().to_internal_value(data)


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
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Pet
        fields = [
            'name', 'breed', 'gender', 'birth_date', 'weight',
            'color', 'chip_number', 'description', 'personality', 'avatar'
        ]


class PetUpdateSerializer(serializers.ModelSerializer):
    """更新宠物序列化器"""
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Pet
        fields = [
            'name', 'breed', 'gender', 'birth_date', 'weight',
            'color', 'chip_number', 'description', 'personality', 'avatar', 'is_active'
        ]