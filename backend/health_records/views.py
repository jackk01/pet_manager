from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from pets.models import Pet
from .models import HealthRecord
from .serializers import HealthRecordSerializer, HealthRecordCreateSerializer


class HealthRecordViewSet(viewsets.ModelViewSet):
    """健康记录视图集"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = HealthRecordSerializer
    
    def get_queryset(self):
        """获取当前用户宠物的健康记录"""
        user_pets = Pet.objects.filter(owner=self.request.user, is_active=True)
        pet_ids = user_pets.values_list('id', flat=True)
        queryset = HealthRecord.objects.filter(pet_id__in=pet_ids)
        
        pet_id = self.request.query_params.get('pet_id')
        if pet_id:
            queryset = queryset.filter(pet_id=pet_id)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return HealthRecordCreateSerializer
        return HealthRecordSerializer
    
    def perform_create(self, serializer):
        pet = serializer.validated_data['pet']
        if pet.owner != self.request.user:
            raise PermissionError("您没有权限为该宠物添加健康记录")
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': '健康记录删除成功'}, status=status.HTTP_200_OK)