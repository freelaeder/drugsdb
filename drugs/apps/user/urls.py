from django.urls import path
# 导包
from apps.user.views import *

urlpatterns = [
    # 判断用户名是否重复注册
    path('user/', UserInfoView.as_view()),
    # 手机号是否重复注册
    path('phone/', PhoneInfoView.as_view()),
    # 用户注册
    path('register/', RegisterView.as_view()),
]
