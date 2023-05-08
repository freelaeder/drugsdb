from django.urls import path
from apps.wxapp.views import *

urlpatterns = [
    # 获取微信用户的图集
    path('getImgs/<username>/', wxGetImgInfo.as_view()),
    # 添加微信用户的图集
    path('postImgs/',wxGetImgInfo.as_view()),
    # 修改喜欢状态
    path('changeImgsLikes/',wxChangeInfo.as_view()),
]
