from django.conf import settings
from django.db import models


class Notification(models.Model):
    """站内信提醒"""

    MESSAGE_TYPES = [
        ('vaccination', '疫苗提醒'),
        ('deworming', '驱虫提醒'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='用户'
    )
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, verbose_name='提醒类型')
    title = models.CharField(max_length=120, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    pet_name = models.CharField(max_length=50, blank=True, verbose_name='宠物名称')
    due_date = models.DateField(null=True, blank=True, verbose_name='到期日期')
    source_model = models.CharField(max_length=30, verbose_name='来源模型')
    source_id = models.PositiveBigIntegerField(verbose_name='来源记录ID')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'notification'
        verbose_name = '站内信提醒'
        verbose_name_plural = '站内信提醒'
        ordering = ['is_read', 'due_date', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'message_type', 'source_model', 'source_id'],
                name='uniq_user_notification_source',
            )
        ]
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', 'due_date']),
        ]

    def __str__(self):
        return f"{self.get_message_type_display()} - {self.title}"
