from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .models import Pet
from .serializers import PetSerializer, PetCreateSerializer, PetUpdateSerializer


class PetViewSet(viewsets.ModelViewSet):
    """宠物管理视图集"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = PetSerializer
    
    def get_queryset(self):
        """获取当前用户的宠物列表"""
        queryset = Pet.objects.filter(owner=self.request.user)
        
        # 是否包含已删除的宠物
        include_inactive = self.request.query_params.get('include_inactive', 'false').lower() == 'true'
        if not include_inactive:
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PetCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PetUpdateSerializer
        return PetSerializer
    
    def perform_create(self, serializer):
        """创建宠物时设置所有者"""
        serializer.save(owner=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """软删除宠物"""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'message': '宠物删除成功'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def count(self, request):
        """统计宠物数量"""
        include_inactive = request.query_params.get('include_inactive', 'false').lower() == 'true'
        queryset = self.get_queryset()
        if not include_inactive:
            queryset = queryset.filter(is_active=True)
        return Response({'count': queryset.count()})