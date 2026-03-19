import calendar
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
    now = timezone.now()
    today = now.date()
    
    # 宠物数量
    pet_count = Pet.objects.filter(owner=user, is_active=True).count()
    
    # 疫苗记录数
    user_pets = Pet.objects.filter(owner=user, is_active=True)
    pet_ids = list(user_pets.values_list('id', flat=True))
    vaccination_count = Vaccination.objects.filter(pet_id__in=pet_ids).count()
    
    # 健康记录数
    health_record_count = HealthRecord.objects.filter(pet_id__in=pet_ids).count()
    
    # 消费总额
    total_expense = Expense.objects.filter(pet_id__in=pet_ids).aggregate(total=Sum('amount'))['total'] or 0
    
    # 即将到期的疫苗数量（30天内）
    end_date = today + timedelta(days=30)
    upcoming_vaccinations_count = Vaccination.objects.filter(
        pet_id__in=pet_ids,
        next_due_date__lte=end_date,
        next_due_date__gte=today
    ).count()
    
    # 本月健康记录数
    month_start = today.replace(day=1)
    monthly_health_records = HealthRecord.objects.filter(
        pet_id__in=pet_ids,
        record_date__gte=month_start
    ).count()
    
    # 本月消费总额
    monthly_total_expense = Expense.objects.filter(
        pet_id__in=pet_ids,
        expense_date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # 计算消费趋势（与上月对比）
    if today.month == 1:
        last_month_start = today.replace(year=today.year - 1, month=12, day=1)
        last_month_end = today.replace(month=1, day=1)
    else:
        last_month_start = today.replace(month=today.month - 1, day=1)
        last_month_end = today.replace(month=today.month, day=1)
    
    last_month_expense = Expense.objects.filter(
        pet_id__in=pet_ids,
        expense_date__gte=last_month_start,
        expense_date__lt=last_month_end
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    if last_month_expense > 0:
        expense_trend = round(((monthly_total_expense - last_month_expense) / last_month_expense) * 100, 1)
    else:
        expense_trend = 0
    
    # 近6个月消费趋势数据
    expense_trend_data = {'months': [], 'amounts': []}
    for i in range(5, -1, -1):
        if today.month - i <= 0:
            month_date = today.replace(year=today.year - 1, month=today.month - i + 12, day=1)
        else:
            month_date = today.replace(month=today.month - i, day=1)
        
        if month_date.month == 12:
            month_end = month_date.replace(year=month_date.year + 1, month=1, day=1)
        else:
            month_end = month_date.replace(month=month_date.month + 1, day=1)
        
        month_expense = Expense.objects.filter(
            pet_id__in=pet_ids,
            expense_date__gte=month_date,
            expense_date__lt=month_end
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        expense_trend_data['months'].append(f"{month_date.month}月")
        expense_trend_data['amounts'].append(float(month_expense))
    
    # 消费类型分布数据
    expense_type_dist = Expense.objects.filter(
        pet_id__in=pet_ids
    ).values('category').annotate(
        total_amount=Sum('amount')
    ).order_by('-total_amount')
    
    category_name_map = {
        'food': '食品',
        'medical': '医疗',
        'grooming': '美容',
        'supplies': '用品',
        'insurance': '保险',
        'other': '其他'
    }
    
    expense_type_data = []
    for item in expense_type_dist:
        expense_type_data.append({
            'type_name': category_name_map.get(item['category'], item['category']),
            'total_amount': float(item['total_amount'] or 0)
        })
    
    return Response({
        'pet_count': pet_count,
        'vaccination_count': vaccination_count,
        'health_record_count': health_record_count,
        'total_expense': total_expense,
        'upcoming_vaccinations_count': upcoming_vaccinations_count,
        'monthly_health_records': monthly_health_records,
        'monthly_total_expense': monthly_total_expense,
        'expense_trend': expense_trend,
        'expense_trend_data': expense_trend_data,
        'expense_type_data': expense_type_data,
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
    """获取完整的消费统计数据"""
    user = request.user
    user_pets = Pet.objects.filter(owner=user, is_active=True)
    pet_ids = list(user_pets.values_list('id', flat=True))
    
    now = timezone.now()
    today = now.date()
    year_start = today.replace(month=1, day=1)
    
    # 总消费金额
    total_expense = Expense.objects.filter(pet_id__in=pet_ids).aggregate(total=Sum('amount'))['total'] or 0
    
    # 平均每月消费
    if total_expense > 0 and today.month > 0:
        avg_monthly_expense = total_expense / today.month
    else:
        avg_monthly_expense = 0
    
    # 疫苗接种次数
    total_vaccinations = Vaccination.objects.filter(pet_id__in=pet_ids).count()
    
    # 健康记录数
    total_health_records = HealthRecord.objects.filter(pet_id__in=pet_ids).count()
    
    # 月度消费趋势
    monthly_trend_data = Expense.objects.filter(
        pet_id__in=pet_ids,
        expense_date__gte=year_start
    ).extra(
        select={'month': "strftime('%%m', expense_date)"}
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('month')
    
    months = []
    amounts = []
    for item in monthly_trend_data:
        month_num = int(item['month'])
        month_name = f"{month_num}月"
        months.append(month_name)
        amounts.append(float(item['total'] or 0))
    
    monthly_trend = {'months': months, 'amounts': amounts}
    
    # 消费类型分布
    expense_type_dist = Expense.objects.filter(
        pet_id__in=pet_ids
    ).values('category').annotate(
        amount=Sum('amount')
    ).order_by('-amount')
    
    # 映射分类名称到中文
    category_name_map = {
        'food': '食品',
        'medical': '医疗',
        'grooming': '美容',
        'supplies': '用品',
        'insurance': '保险',
        'other': '其他'
    }
    
    expense_type_distribution = []
    for item in expense_type_dist:
        type_name = category_name_map.get(item['category'], item['category'])
        expense_type_distribution.append({
            'type': type_name,
            'amount': float(item['amount'] or 0)
        })
    
    # 宠物消费占比
    pet_expense_dist = Expense.objects.filter(
        pet_id__in=pet_ids
    ).values('pet__name').annotate(
        amount=Sum('amount')
    ).order_by('-amount')
    
    pet_expense_distribution = []
    for item in pet_expense_dist:
        pet_name = item['pet__name'] or '未知宠物'
        pet_expense_distribution.append({
            'pet_name': pet_name,
            'amount': float(item['amount'] or 0)
        })
    
    # 健康记录类型分布
    health_type_dist = HealthRecord.objects.filter(
        pet_id__in=pet_ids
    ).values('record_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    health_type_distribution = []
    for item in health_type_dist:
        health_type_distribution.append({
            'type': item['record_type'],
            'count': item['count']
        })
    
    # 年度消费明细（按月分组）
    yearly_detail_months = []
    yearly_detail_food = []
    yearly_detail_medical = []
    yearly_detail_beauty = []
    yearly_detail_other = []
    
    # 分类映射
    cat_map = {
        'food': 'food',
        'medical': 'medical',
        'grooming': 'beauty',
    }
    
    for month in range(1, today.month + 1):
        month_start = today.replace(month=month, day=1)
        if month == 12:
            month_end = today.replace(year=today.year + 1, month=1, day=1)
        else:
            month_end = today.replace(month=month + 1, day=1)
        
        monthly_expenses = Expense.objects.filter(
            pet_id__in=pet_ids,
            expense_date__gte=month_start,
            expense_date__lt=month_end
        )
        
        yearly_detail_months.append(f"{month}月")
        
        # 按分类汇总
        food_total = monthly_expenses.filter(category='food').aggregate(total=Sum('amount'))['total'] or 0
        medical_total = monthly_expenses.filter(category='medical').aggregate(total=Sum('amount'))['total'] or 0
        grooming_total = monthly_expenses.filter(category='grooming').aggregate(total=Sum('amount')) or 0
        other_total = monthly_expenses.exclude(category__in=['food', 'medical', 'grooming']).aggregate(total=Sum('amount'))['total'] or 0
        
        yearly_detail_food.append(float(food_total))
        yearly_detail_medical.append(float(medical_total))
        yearly_detail_beauty.append(float(grooming_total.get('total', 0) or 0))
        yearly_detail_other.append(float(other_total))
    
    yearly_detail = {
        'months': yearly_detail_months,
        'food': yearly_detail_food,
        'medical': yearly_detail_medical,
        'beauty': yearly_detail_beauty,
        'other': yearly_detail_other
    }
    
    return Response({
        'total_expense': total_expense,
        'avg_monthly_expense': round(avg_monthly_expense, 2),
        'total_vaccinations': total_vaccinations,
        'total_health_records': total_health_records,
        'monthly_trend': monthly_trend,
        'expense_type_distribution': expense_type_distribution,
        'pet_expense_distribution': pet_expense_distribution,
        'health_type_distribution': health_type_distribution,
        'yearly_detail': yearly_detail
    })