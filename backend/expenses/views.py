from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from pets.models import Pet
from .models import Expense
from .serializers import ExpenseSerializer, ExpenseCreateSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    """消费记录视图集"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer
    
    def get_queryset(self):
        """获取当前用户宠物的消费记录"""
        user_pets = Pet.objects.filter(owner=self.request.user, is_active=True)
        pet_ids = user_pets.values_list('id', flat=True)
        queryset = Expense.objects.filter(pet_id__in=pet_ids)
        
        pet_id = self.request.query_params.get('pet_id')
        if pet_id:
            queryset = queryset.filter(pet_id=pet_id)
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ExpenseCreateSerializer
        return ExpenseSerializer
    
    def perform_create(self, serializer):
        pet = serializer.validated_data['pet']
        if pet.owner != self.request.user:
            raise PermissionError("您没有权限为该宠物添加消费记录")
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': '消费记录删除成功'}, status=status.HTTP_200_OK)