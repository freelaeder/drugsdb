from django.urls import path
# 导包
from apps.user.views import *

urlpatterns = [
    # 测试
    path('user/', UserInfoView.as_view()),
]
