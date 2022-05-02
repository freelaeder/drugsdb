from django.urls import path
# 导包
from rest_framework.routers import DefaultRouter

from apps.user.views import *

urlpatterns = [
    # 判断用户名是否重复注册
    path('user/', UserInfoView.as_view()),
    # 手机号是否重复注册
    path('phone/', PhoneInfoView.as_view()),
    # 用户注册
    path('register/', RegisterView.as_view()),
    # 用户登录
    path('login/', LoginView.as_view()),
    # 保存用户基本信息 改用序列化器
    path('saveinfo/', SaveInfo.as_view()),
    # 保存图片
    path('upload/', SaveImg.as_view()),
]

# 保存用户基本信息 改用序列化器
router = DefaultRouter()
# 获取用户数据
router.register(prefix='getinfo', viewset=UserSaveModel, basename='getinfos')
# 把路由添加到urlpatterns
urlpatterns += router.urls
