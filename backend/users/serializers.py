import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    class Base64ImageField(serializers.ImageField):
        def to_internal_value(self, data):
            if data in (None, '', 'null', 'undefined'):
                return None

            if isinstance(data, str) and data.startswith('data:image'):
                format_part, image_data = data.split(';base64,')
                ext = format_part.split('/')[-1]
                filename = f"{uuid.uuid4().hex}.{ext}"
                data = ContentFile(base64.b64decode(image_data), name=filename)
            elif isinstance(data, str):
                return None

            return super().to_internal_value(data)

    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'nickname', 'avatar', 'phone',
            'is_active', 'last_login', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avatar'] = instance.avatar.url if instance.avatar else None
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'nickname', 'phone']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "两次输入的密码不一致"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            nickname=validated_data.get('nickname', ''),
            phone=validated_data.get('phone', ''),
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码错误")
        return value


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
