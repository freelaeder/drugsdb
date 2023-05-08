from django.urls import path

from apps.blog.views import ShowArticleList, GetArticleDetail, GetArticleSortAll, GetArticleTagAll, SaveArtcile, \
    GetHotArticlePage, GetArticleAll2

urlpatterns = [
    # 获取列表页
    path('article/queryArticlePage', ShowArticleList.as_view()),
    # 获取指定页数据
    #  article/queryArticleByUid/ae29d4d0-55a3-11ec-96d5-7933aca11ca0
    path('article/queryArticleByUid/<uid>', GetArticleDetail.as_view()),
    # articleSort/queryArticleSortAll
    # 获取全部标签
    path('articleSort/queryArticleSortAll', GetArticleSortAll.as_view()),
    # 获取全部的blog tag 标签
    # articleTag/queryArticleTagAll
    path('articleTag/queryArticleTagAll', GetArticleTagAll.as_view()),
    # blog类别页获取hot分类标签  articleTag/queryHotArticleTagPage
    path('articleTag/queryHotArticleTagPage', GetArticleTagAll.as_view()),
    # 保存
    path('article/saveArticle', SaveArtcile.as_view()),
    # article/queryHotArticlePage
    path('article/queryHotArticlePage', GetHotArticlePage.as_view()),
    # article/queryArticleAll2
    path('article/queryArticleAll2', GetArticleAll2.as_view()),
]
