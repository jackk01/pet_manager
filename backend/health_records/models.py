from django.db import models
from pets.models import Pet


class HealthRecord(models.Model):
    """健康记录模型"""
    
    RECORD_TYPES = [
        ('就诊', '就诊'),
        ('体检', '体检'),
        ('体重', '体重'),
        ('驱虫', '驱虫'),
        ('过敏', '过敏'),
        ('手术', '手术'),
        ('其他', '其他'),
    ]
    
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='health_records',
        verbose_name="宠物"
    )
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES, verbose_name="记录类型")
    record_date = models.DateField(verbose_name="记录日期")
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(blank=True, verbose_name="详细内容")
    hospital = models.CharField(max_length=100, blank=True, verbose_name="医院名称")
    doctor = models.CharField(max_length=50, blank=True, verbose_name="医生姓名")
    cost = models.FloatField(null=True, blank=True, verbose_name="费用")
    attachment = models.FileField(upload_to='health_records/', blank=True, verbose_name="附件")
    next_check_date = models.DateField(null=True, blank=True, verbose_name="下次复查日期")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'health_record'
        verbose_name = '健康记录'
        verbose_name_plural = '健康记录'
        ordering = ['-record_date']
    
    def __str__(self):
        return f"{self.title} - {self.pet.name}"