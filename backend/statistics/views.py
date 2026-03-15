from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Sum

from pets.models import Pet
from vaccinations.models import Vaccination
from health_records.models import HealthRecord
from expenses.models import Expense


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    """获取仪表盘统计数据"""
    user = request.user
    
    # 宠物数量
    pet_count = Pet.objects.filter(owner=user, is_active=True).count()
    
    # 疫苗记录数
    user_pets = Pet.objects.filter(owner=user, is_active=True)
    pet_ids = user_pets.values_list('id', flat=True)
    vaccination_count = Vaccination.objects.filter(pet_id__in=pet_ids).count()
    
    # 健康记录数
    health_record_count = HealthRecord.objects.filter(pet_id__in=pet_ids).count()
    
    # 消费总额
    total_expense = Expense.objects.filter(pet_id__in=pet_ids).aggregate(total=Sum('amount'))['total'] or 0
    
    return Response({
        'pet_count': pet_count,
        'vaccination_count': vaccination_count,
        'health_record_count': health_record_count,
        'total_expense': total_expense,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def upcoming_vaccinations(request):
    """获取即将到期的疫苗记录"""
    days = int(request.query_params.get('days', 30))
    end_date = timezone.now().date() + timedelta(days=days)
    
    user_pets = Pet.objects.filter(owner=request.user, is_active=True)
    pet_ids = user_pets.values_list('id', flat=True)
    
    vaccinations = Vaccination.objects.filter(
        pet_id__in=pet_ids,
        next_due_date__lte=end_date,
        next_due_date__gte=timezone.now().date()
    ).select_related('pet')[:20]
    
    results = []
    for v in vaccinations:
        results.append({
            'id': v.id,
            'pet_id': v.pet.id,
            'pet_name': v.pet.name,
            'vaccine_name': v.vaccine_name,
            'vaccination_date': v.vaccination_date,
            'next_due_date': v.next_due_date,
            'clinic': v.clinic,
        })
    
    return Response(results)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_health_records(request):
    """获取最近的健康记录"""
    limit = int(request.query_params.get('limit', 5))
    
    user_pets = Pet.objects.filter(owner=request.user, is_active=True)
    pet_ids = user_pets.values_list('id', flat=True)
    
    records = HealthRecord.objects.filter(
        pet_id__in=pet_ids
    ).select_related('pet').order_by('-record_date')[:limit]
    
    results = []
    for r in records:
        results.append({
            'id': r.id,
            'pet_id': r.pet.id,
            'pet_name': r.pet.name,
            'record_type': r.record_type,
            'record_date': r.record_date,
            'title': r.title,
            'hospital': r.hospital,
            'doctor': r.doctor,
            'cost': r.cost,
        })
    
    return Response(results)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_statistics(request):
    """获取消费统计"""
    user_pets = Pet.objects.filter(owner=request.user, is_active=True)
    pet_ids = user_pets.values_list('id', flat=True)
    
    # 按分类统计
    category_stats = Expense.objects.filter(
        pet_id__in=pet_ids
    ).values('category').annotate(
        total=Sum('amount'),
        count=Count('id')
    )
    
    # 总计
    total = Expense.objects.filter(pet_id__in=pet_ids).aggregate(total=Sum('amount'))['total'] or 0
    
    return Response({
        'total': total,
        'by_category': list(category_stats),
    })