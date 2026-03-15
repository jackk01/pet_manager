from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """自定义用户模型"""

    nickname = models.CharField(max_length=50, blank=True, verbose_name="昵称")
    phone = models.CharField(max_length=20, blank=True, verbose_name="手机号码")
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name="头像")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
    
    def __str__(self):
        return self.username