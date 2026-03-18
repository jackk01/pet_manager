from datetime import timedelta
from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
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
        
        # 支持日期范围筛选
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(expense_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(expense_date__lte=end_date)
        
        return queryset.order_by('-expense_date')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ExpenseCreateSerializer
        return ExpenseSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # 分页
        page = int(request.query_params.get('page', 1))
        size = int(request.query_params.get('size', 10))
        start = (page - 1) * size
        end = start + size
        
        total = queryset.count()
        items = queryset[start:end]
        
        serializer = self.get_serializer(items, many=True)
        return Response({
            'items': serializer.data,
            'total': total
        })
    
    def perform_create(self, serializer):
        pet = serializer.validated_data['pet']
        if pet.owner != self.request.user:
            raise PermissionError("您没有权限为该宠物添加消费记录")
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': '消费记录删除成功'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_stats(request):
    """获取消费统计数据"""
    user_pets = Pet.objects.filter(owner=request.user, is_active=True)
    pet_ids = list(user_pets.values_list('id', flat=True))
    
    now = timezone.now()
    today = now.date()
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)
    
    # 本月总消费
    monthly_total = Expense.objects.filter(
        pet_id__in=pet_ids,
        expense_date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # 年度总消费
    yearly_total = Expense.objects.filter(
        pet_id__in=pet_ids,
        expense_date__gte=year_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # 累计总消费
    total = Expense.objects.filter(
        pet_id__in=pet_ids
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # 计算平均每月消费
    if yearly_total > 0:
        months_passed = today.month
        average_monthly = yearly_total / months_passed if months_passed > 0 else yearly_total
    else:
        average_monthly = 0
    
    return Response({
        'monthly_total': monthly_total,
        'yearly_total': yearly_total,
        'total': total,
        'average_monthly': round(average_monthly, 2)
    })