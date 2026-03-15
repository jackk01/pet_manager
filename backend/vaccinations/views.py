from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from pets.models import Pet
from .models import Vaccination
from .serializers import VaccinationSerializer, VaccinationCreateSerializer


class VaccinationViewSet(viewsets.ModelViewSet):
    """疫苗记录视图集"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = VaccinationSerializer
    
    def get_queryset(self):
        """获取当前用户宠物的疫苗记录"""
        # 先获取用户的所有宠物
        user_pets = Pet.objects.filter(owner=self.request.user, is_active=True)
        
        # 再获取这些宠物的疫苗记录
        pet_ids = user_pets.values_list('id', flat=True)
        queryset = Vaccination.objects.filter(pet_id__in=pet_ids)
        
        # 可按宠物筛选
        pet_id = self.request.query_params.get('pet_id')
        if pet_id:
            queryset = queryset.filter(pet_id=pet_id)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return VaccinationCreateSerializer
        return VaccinationSerializer
    
    def perform_create(self, serializer):
        """验证宠物属于当前用户后保存"""
        pet = serializer.validated_data['pet']
        if pet.owner != self.request.user:
            raise PermissionError("您没有权限为该宠物添加疫苗记录")
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        """删除疫苗记录"""
        instance = self.get_object()
        instance.delete()
        return Response({'message': '疫苗记录删除成功'}, status=status.HTTP_200_OK)