from django.db import models
from pets.models import Pet


class Vaccination(models.Model):
    """疫苗记录模型"""
    
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='vaccinations',
        verbose_name="宠物"
    )
    vaccine_name = models.CharField(max_length=100, verbose_name="疫苗名称")
    vaccination_date = models.DateField(verbose_name="接种日期")
    next_due_date = models.DateField(null=True, blank=True, verbose_name="下次接种日期")
    clinic = models.CharField(max_length=100, blank=True, verbose_name="接种单位")
    doctor = models.CharField(max_length=50, blank=True, verbose_name="医生姓名")
    batch_number = models.CharField(max_length=50, blank=True, verbose_name="疫苗批次号")
    remark = models.TextField(blank=True, verbose_name="备注")
    attachment = models.FileField(upload_to='vaccinations/', blank=True, verbose_name="附件")
    is_reminded = models.BooleanField(default=False, verbose_name="是否已提醒")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'vaccination'
        verbose_name = '疫苗记录'
        verbose_name_plural = '疫苗记录'
        ordering = ['-vaccination_date']
    
    def __str__(self):
        return f"{self.vaccine_name} - {self.pet.name}"