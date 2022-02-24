from django.urls import path
# 导包
from apps.verifications.views import *

urlpatterns = [
    # 返回图形验证码
    path('image_codes/', ImageCodeView.as_view()),
    # 验证用户输入图形验证码是否正确
    path('image_codes_info/', ImageCodeInfoView.as_view()),

]
