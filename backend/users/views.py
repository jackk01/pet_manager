from django.db.models import Sum
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError

from pets.models import Pet
from vaccinations.models import Vaccination
from health_records.models import HealthRecord
from expenses.models import Expense

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    ChangePasswordSerializer,
    LoginSerializer
)

User = get_user_model()


class RegisterView(APIView):
    """用户注册"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'nickname': user.nickname,
                    'avatar': user.avatar.url if user.avatar else None,
                    'phone': user.phone,
                    'is_active': user.is_active,
                    'created_at': user.created_at.isoformat(),
                    'updated_at': user.updated_at.isoformat(),
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {'error': '用户名或邮箱已存在'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """用户登录"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user is None:
                # Try email login
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is None:
                return Response(
                    {'error': '用户名或密码错误'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not user.is_active:
                return Response(
                    {'error': '用户已被禁用'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'token_type': 'bearer',
                'expires_in': 1800,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """用户资料"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取当前用户资料"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """更新当前用户资料"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """修改密码"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'message': '密码修改成功'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """获取用户统计数据"""
    user = request.user
    
    # 宠物数量
    pet_count = Pet.objects.filter(owner=user, is_active=True).count()
    
    # 用户所有宠物的ID列表
    user_pets = Pet.objects.filter(owner=user, is_active=True)
    pet_ids = list(user_pets.values_list('id', flat=True))
    
    # 疫苗记录数
    vaccination_count = Vaccination.objects.filter(pet_id__in=pet_ids).count()
    
    # 健康记录数
    health_record_count = HealthRecord.objects.filter(pet_id__in=pet_ids).count()
    
    # 总消费
    total_expense = Expense.objects.filter(pet_id__in=pet_ids).aggregate(total=Sum('amount'))['total'] or 0
    
    return Response({
        'pet_count': pet_count,
        'vaccination_count': vaccination_count,
        'health_record_count': health_record_count,
        'total_expense': total_expense
    })


class UserSettingsView(APIView):
    """用户设置"""
    permission_classes = [IsAuthenticated]
    
    # 默认设置
    DEFAULT_SETTINGS = {
        'email_notification': True,
        'sms_notification': False,
        'remind_days': 7,
        'language': 'zh-CN',
        'theme': 'light'
    }
    
    def get(self, request):
        """获取用户设置"""
        # 从用户模型中获取设置（目前使用默认设置）
        # 实际项目中可以添加UserSettings模型来存储用户设置
        settings = getattr(request.user, 'settings', None)
        if settings:
            return Response(settings)
        return Response(self.DEFAULT_SETTINGS)
    
    def put(self, request):
        """更新用户设置"""
        # 实际项目中应该保存到数据库
        # 这里简单返回成功消息
        return Response({
            'email_notification': request.data.get('email_notification', True),
            'sms_notification': request.data.get('sms_notification', False),
            'remind_days': request.data.get('remind_days', 7),
            'language': request.data.get('language', 'zh-CN'),
            'theme': request.data.get('theme', 'light')
        })