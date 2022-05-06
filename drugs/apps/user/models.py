# Create your models here.
from django.db import models

from django.contrib.auth.models import AbstractUser


# 用户表
class User(AbstractUser):
    # 性别选择
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    mobile = models.CharField(max_length=11, unique=True)
    # 技术栈
    tecs = models.CharField(default='', max_length=100)
    # 添加邮箱字段
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    default_address = models.IntegerField(null=True, blank=True, verbose_name='默认地址', )
    # 学校
    school = models.CharField(max_length=20, verbose_name='学校', default='北京邮电大学')
    # 性别
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    # 个人签名
    description = models.CharField(max_length=200, null=True, verbose_name='描述信息')
    # 用户头像
    default_image = models.ImageField(max_length=200, default='', null=True, blank=True, verbose_name='默认图片')
    # 展示图片
    show_image = models.ImageField(max_length=200, default='', null=True, blank=True, verbose_name='展示图片')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

