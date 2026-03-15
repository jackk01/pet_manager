from django.db import models
from pets.models import Pet


class Expense(models.Model):
    """消费记录模型"""
    
    CATEGORIES = [
        ('food', '食物'),
        ('medical', '医疗'),
        ('grooming', '美容'),
        ('supplies', '用品'),
        ('insurance', '保险'),
        ('other', '其他'),
    ]
    
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name="宠物"
    )
    category = models.CharField(max_length=20, choices=CATEGORIES, verbose_name="消费分类")
    expense_date = models.DateField(verbose_name="消费日期")
    amount = models.FloatField(verbose_name="金额")
    merchant = models.CharField(max_length=100, blank=True, verbose_name="商家名称")
    remark = models.TextField(blank=True, verbose_name="备注")
    attachment = models.FileField(upload_to='expenses/', blank=True, verbose_name="小票/凭证")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'expense'
        verbose_name = '消费记录'
        verbose_name_plural = '消费记录'
        ordering = ['-expense_date']
    
    def __str__(self):
        return f"{self.amount}元 - {self.pet.name}"