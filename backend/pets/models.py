from django.db import models
from django.conf import settings


class Pet(models.Model):
    """宠物模型"""
    
    GENDER_CHOICES = [
        ('公', '公'),
        ('母', '母'),
        ('未知', '未知'),
    ]
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pets',
        verbose_name="所属用户"
    )
    name = models.CharField(max_length=50, verbose_name="宠物名称")
    breed = models.CharField(max_length=100, blank=True, verbose_name="品种")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, verbose_name="性别")
    birth_date = models.DateField(null=True, blank=True, verbose_name="出生日期")
    weight = models.FloatField(null=True, blank=True, verbose_name="体重(kg)")
    color = models.CharField(max_length=50, blank=True, verbose_name="毛色")
    chip_number = models.CharField(max_length=50, blank=True, verbose_name="芯片号")
    description = models.TextField(blank=True, verbose_name="特征描述")
    personality = models.TextField(blank=True, verbose_name="性格特点")
    avatar = models.ImageField(upload_to='pets/', blank=True, verbose_name="宠物头像")
    is_active = models.BooleanField(default=True, verbose_name="是否有效")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'pet'
        verbose_name = '宠物'
        verbose_name_plural = '宠物'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name