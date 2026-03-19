from datetime import timedelta

from django.utils import timezone

from health_records.models import HealthRecord
from vaccinations.models import Vaccination

from .models import Notification


def _get_status_text(days_left: int) -> str:
    if days_left < 0:
        return f'已逾期{abs(days_left)}天'
    if days_left == 0:
        return '今天到期'
    return f'{days_left}天后到期'


def sync_user_notifications(user, days: int = 14) -> None:
    """根据疫苗/驱虫数据同步用户站内信"""

    days = max(1, min(days, 90))
    today = timezone.now().date()
    window_start = today - timedelta(days=30)
    window_end = today + timedelta(days=days)

    valid_keys = set()

    vaccinations = Vaccination.objects.filter(
        pet__owner=user,
        pet__is_active=True,
        next_due_date__isnull=False,
        next_due_date__gte=window_start,
        next_due_date__lte=window_end,
    ).select_related('pet')

    for item in vaccinations:
        days_left = (item.next_due_date - today).days
        title = f"{item.pet.name} 疫苗提醒"
        content = f"{item.vaccine_name} {_get_status_text(days_left)}，请及时安排接种。"
        Notification.objects.update_or_create(
            user=user,
            message_type='vaccination',
            source_model='vaccination',
            source_id=item.id,
            defaults={
                'title': title,
                'content': content,
                'pet_name': item.pet.name,
                'due_date': item.next_due_date,
            },
        )
        valid_keys.add(('vaccination', 'vaccination', item.id))

    deworming_records = HealthRecord.objects.filter(
        pet__owner=user,
        pet__is_active=True,
        record_type='驱虫',
        next_check_date__isnull=False,
        next_check_date__gte=window_start,
        next_check_date__lte=window_end,
    ).select_related('pet')

    for item in deworming_records:
        days_left = (item.next_check_date - today).days
        title = f"{item.pet.name} 驱虫提醒"
        content = f"{item.title or '驱虫计划'} {_get_status_text(days_left)}，建议按时执行。"
        Notification.objects.update_or_create(
            user=user,
            message_type='deworming',
            source_model='health_record',
            source_id=item.id,
            defaults={
                'title': title,
                'content': content,
                'pet_name': item.pet.name,
                'due_date': item.next_check_date,
            },
        )
        valid_keys.add(('deworming', 'health_record', item.id))

    existing = Notification.objects.filter(user=user, message_type__in=['vaccination', 'deworming'])
    for item in existing:
        key = (item.message_type, item.source_model, item.source_id)
        if key not in valid_keys:
            item.delete()
