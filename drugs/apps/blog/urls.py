from django.urls import path

from apps.blog.views import ShowArticleList

urlpatterns = [
    path('article/queryArticlePage', ShowArticleList.as_view()),

]
