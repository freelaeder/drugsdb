from django.urls import path

from apps.blog.views import ShowArticleList, GetArticleDetail

urlpatterns = [
    # 获取blog列表页
    path('article/queryArticlePage', ShowArticleList.as_view()),
    # 获取blog指定页数据
    #  article/queryArticleByUid/ae29d4d0-55a3-11ec-96d5-7933aca11ca0
    path('article/queryArticleByUid/<uid>', GetArticleDetail.as_view()),

]
