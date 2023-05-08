import json

import pytz
from django.db import transaction
from django.http import JsonResponse
import uuid

# Create your views here.
from django.utils import timezone
from django.views import View
# 连接数据库
from pymysql import connect

from apps.blog.models import TBlog, TBlogSort, MtBlogBlogTag, TBlogTag
# 分页
from django.core.paginator import Paginator


class ShowArticleList(View):
    # 获取列表详情页

    def post(self, request):
        data_dict = json.loads(request.body)
        print(data_dict)
        # {'blogStatus': 1, 'currentPage': 1, 'pageSize': 20}
        # blog的状态
        blogStatus = data_dict.get('blogStatus')
        # 当前是第几次请求
        currentPage = data_dict.get('currentPage')
        # 请求的页数
        pageSize = data_dict.get('pageSize')
        # 创建Connection连接mysql
        conn = connect(host='127.0.0.1', port=3306, database='blogdb', user='root', password='mysql',
                       charset='utf8')
        # 获得Cursor对象
        cs1 = conn.cursor()
        # 根据pagesize
        # 请求sql
        try:
            blog_data = cs1.execute(
                'select d.uid,d.blog_title,d.blog_summary,d.blog_content,d.create_time,s.sort_name,d.cover_url from t_blog as d left join t_blog_sort as s on d.blog_sort_id = s.uid order by d.create_time desc')
            # 打印获取的行数
            # print(blog_data)
            # 获取全部
            # 转化为数组
            blog_list = list(cs1.fetchall())
            # 10 条为一页
            item = Paginator(blog_list, pageSize)
            # 获取当前数组的长度
            item_length = len(item.page(currentPage).object_list)
            print(item_length, '当前数组长度')

            result = []
            # 遍历要根据获取的数组长度遍历，不能根据pageSize ，万一没有数据，该程序报错
            for i in range(item_length):
                result.append({
                    'blog_sort_id': item.page(currentPage).object_list[i][0],
                    'blog_title': item.page(currentPage).object_list[i][1],
                    'blog_summary': item.page(currentPage).object_list[i][2],
                    'blog_content': item.page(currentPage).object_list[i][3],
                    'create_time': item.page(currentPage).object_list[i][4],
                    'sort_name': item.page(currentPage).object_list[i][5],
                    'cover_url': item.page(currentPage).object_list[i][6],
                    'uid': item.page(currentPage).object_list[i][0],
                })

            # 拼接数据返回
            # 获取blog的总数
            blog_num = TBlog.objects.count()
            data = {
                'currentPage': currentPage,
                'pageSize': pageSize,
                'total': blog_num,
                'result': result,
            }
        except Exception as e:
            print(e)
            return JsonResponse({'code': 405, 'msg': '数据已经全部返回', 'data': data})

        return JsonResponse({'code': 1, 'msg': 'ok', 'data': data})


# 获取指定页数据
class GetArticleDetail(View):
    def get(self, request, uid):
        print(uid)
        # 连接数据库查询返回
        try:
            result = []

            data = TBlog.objects.filter(uid=uid)
            # print(type(uid))
            # 获取sort_id 以下两种都可以
            # 获取 sort_name
            sort_id = TBlog.objects.filter(uid=uid).values('blog_sort_id').values()[0].get('blog_sort_id')
            # print(sort_id, 'sort_id')
            # sort_id = TBlog.objects.get(uid=uid)
            # print(sort_id.blog_sort_id)

            sort_name = TBlogSort.objects.get(uid=sort_id)
            # 获取 sort_name
            sort_name = sort_name.sort_name
            # print(sort_name, 'sort_name')
            # 获取tag
            tag_id = MtBlogBlogTag.objects.filter(blog_id=uid)
            print(tag_id, 'tag_id')
            # 假如有多个先储存起来，再一一获取tag名字
            # tag_list = []
            # 定义返回的列表
            blog_tags = []
            for item in tag_id:
                blog_tags.append({
                    'blog_tag_id': item.blog_tag_id,
                    'tag_name': TBlogTag.objects.filter(uid=item.blog_tag_id).values()[0].get('tag_name'),
                })
                # tag_list.append(item.blog_tag_id)
                print(TBlogTag.objects.filter(uid=item.blog_tag_id).values()[0])
                # {'uid': '3b767f40-2cbf-11ec-86ae-0da8227970f6', 'tag_name': 'js', 'clicks': 0,
                # 'order_num': 0, 'create_time': '2021-10-14 15:20:38', 'update_time': '2021-10-14 15:20:38'}
                print(TBlogTag.objects.filter(uid=item.blog_tag_id).values('tag_name')[0])
                # {'tag_name': 'js'}  values 指定字段
                print(TBlogTag.objects.filter(uid=item.blog_tag_id).values()[0].get('tag_name'))
            #     js
            # print(tag_list)

            for item in data:
                result.append({
                    'uid': item.uid,
                    'blog_author_id': item.blog_author_id,
                    'blog_content': item.blog_content,
                    'blog_title': item.blog_title,
                    'create_time': item.create_time,
                    'cover_url': item.cover_url,
                    'blod_summary': item.blog_summary,
                    'update_time': item.update_time,
                    'sort_name': sort_name,
                    'blog_tags': blog_tags,
                    'clicks': item.clicks,
                    'order_num': item.order_num,

                })

        except Exception as e:
            print(e)
            return JsonResponse({'code': 404, 'msg': 'defeated', })
        return JsonResponse({'code': 1, 'msg': 'success', 'data': result})


# 获取全部的文章分类标签
class GetArticleSortAll(View):

    def post(self, request):
        result = []
        # 连接数据库返回数据
        try:
            sort_data = TBlogSort.objects.all()
            for item in sort_data:
                result.append({
                    'clicks': item.clicks,
                    'create_time': item.create_time,
                    'intro': item.intro,
                    'order_num': item.order_num,
                    'sort_name': item.sort_name,
                    'uid': item.uid,
                    'update_time': item.update_time,
                })
        except Exception as e:
            print(e)
            return JsonResponse({'code': 500, 'msg': 'defeated', 'data': '服务器错误'})

        return JsonResponse({'code': 1, 'msg': 'success', 'data': result})


#
class GetArticleTagAll(View):
    def post(self, request):
        # 连接数据库返回数据
        try:
            tb_data = TBlogTag.objects.all()
            # 定义数组格式化数据
            result = []
            for item in tb_data:
                result.append({
                    'clicks': item.clicks,
                    'create_time': item.create_time,
                    'order_num': item.order_num,
                    'tag_name': item.tag_name,
                    'uid': item.uid,
                    'update_time': item.update_time,
                })

        except Exception as e:
            print(e)
            return JsonResponse({'code': 500, 'msg': 'defeated', 'data': '服务器错误'})

        return JsonResponse({'code': 1, 'msg': 'success', 'data': result})


# 保存博客
class SaveArtcile(View):
    def post(self, request):
        data = {}
        # 获取当前时间  utc 时间
        # d1 = timezone.now()
        # print(d1)
        # 直接获取当地时间  格式化
        cn = pytz.timezone('Asia/Shanghai')
        # 当前时间
        d2 = timezone.now().astimezone(tz=cn).strftime("%Y-%m-%d %H:%M:%S")
        print(d2)
        # 2022-05-05 23:24:17
        # 根据当地的时间动态生成uuid，保证该uuid不会重复
        uuid_data = uuid.uuid3(uuid.NAMESPACE_DNS, d2)
        print(f'uuid_data-------------------------{uuid_data}')
        # 开启事务
        with transaction.atomic():
            # 创建事务回滚点
            save_id = transaction.savepoint()
            try:

                # 先获取数据 ，创建t_blog 在根据uuid创建 mt_blog_blog_tag
                blog_data = json.loads(request.body)
                # 博客内容
                blogContent = blog_data.get('blogContent')
                # 博客分类
                blogSortId = blog_data.get('blogSortId')
                # 博客状态 1 发布；2 下架；3 草稿；
                blogStatus = blog_data.get('blogStatus')
                # 博客介绍
                blogSummary = blog_data.get('blogSummary')
                # 博客标签
                blogTagIds = blog_data.get('blogTagIds')
                # 博客标题
                blogTitle = blog_data.get('blogTitle')
                # 博客展示图片
                coverUrl = blog_data.get('coverUrl')
                # 是否评论 ：1 开启；2 关闭',
                isOpenComment = blog_data.get('isOpenComment')
                # 是否为私密文章 ：1 是；2 否',
                isPrivate = blog_data.get('isPrivate')
                # 是否原创 1 原创；2转载；3 翻译
                isOriginal = blog_data.get('isOriginal')
                # 排序
                order = blog_data.get('order')
                # 文章来源地址
                originAddress = blog_data.get('originAddress') if blog_data.get('originAddress') else ""
                # 推荐等级
                recommendLevel = blog_data.get('recommendLevel')
                # 判断参数是否完整
                if not all(
                        [blogContent, blogSummary, blogStatus, blogSortId, blogTagIds, blogTitle, coverUrl, isOriginal,
                         isOpenComment, isPrivate, order, recommendLevel]):
                    return JsonResponse({'code': 404, 'msg': 'defeated', 'data': '参数不够'})
                # 创建博客详情表数据
                TBlog.objects.create(
                    uid=uuid_data, blog_title=blogTitle, blog_summary=blogSummary, is_original=isOriginal,
                    origin_address=originAddress, blog_sort_id=blogSortId, recommend_level=recommendLevel,
                    order_num=order, is_open_comment=isOpenComment, is_private=isPrivate, blog_status=blogStatus,
                    cover_url=coverUrl, blog_content=blogContent, create_time=d2, update_time=d2, clicks=0
                )
                # 根据博客在创建该博客的标签，移至else

            except Exception as e:
                print(e)
                transaction.savepoint_rollback(save_id)
                return JsonResponse({'code': 500, 'msg': 'defeated', 'data': '服务器错误'})
            else:
                #  # 根据博客在创建该博客的标签，
                # 遍历blogTagIds
                for item in blogTagIds:
                    MtBlogBlogTag.objects.create(blog_id=uuid_data, blog_tag_id=item, create_time=d2, update_time=d2,
                                                 blog_is_private=isPrivate)

            # 提交成功，显示提交事务
            transaction.savepoint_commit(save_id)

        return JsonResponse({'code': 1, 'msg': 'success', 'data': data})


class GetHotArticlePage(View):
    # 获取点击排行
    def post(self, request):
        try:
            data = TBlog.objects.order_by('-clicks')[:5]
            result = []
            for item in data:
                result.append({
                    'blog_author_id': item.blog_author_id,
                    'blog_content': item.blog_content,
                    'blog_sort_id': item.blog_sort_id,
                    'blog_status': item.blog_status,
                    'blog_summary': item.blog_summary,
                    'blog_title': item.blog_title,
                    'clicks': item.clicks,
                    'cover_url': item.cover_url,
                    'create_time': item.create_time,
                    'is_open_comment': item.is_open_comment,
                    'is_original': item.is_original,
                    'is_private': item.is_private,
                    'order_num': item.order_num,
                    'origin_address': item.origin_address,
                    'recommend_level': item.recommend_level,
                    'uid': item.uid,
                    'update_time': item.update_time,
                })

            # print(data)

        except Exception as e:
            print(e)
            return JsonResponse({'code': 500, 'msg': 'defeated', })
        return JsonResponse({'code': 1, 'msg': 'success', 'data': result})


# GetArticleAll2 获取推荐等级数据
class GetArticleAll2(View):
    def post(self, request):
        # 获取数据
        data_dict = json.loads(request.body)
        # 获取推荐等级
        recommendLevel = data_dict.get('recommendLevel')
        if not recommendLevel:
            return JsonResponse({'code': 404, 'msg': '参数错误', })

        result = []
        try:
            data = TBlog.objects.filter(recommend_level=recommendLevel).order_by('-create_time', 'order_num')[
                   :recommendLevel + 1]
            result = []
            for item in data:
                result.append({
                    'blog_author_id': item.blog_author_id,
                    'blog_content': item.blog_content,
                    'blog_sort_id': item.blog_sort_id,
                    'blog_status': item.blog_status,
                    'blog_summary': item.blog_summary,
                    'blog_title': item.blog_title,
                    'clicks': item.clicks,
                    'cover_url': item.cover_url,
                    'create_time': item.create_time,
                    'is_open_comment': item.is_open_comment,
                    'is_original': item.is_original,
                    'is_private': item.is_private,
                    'order_num': item.order_num,
                    'origin_address': item.origin_address,
                    'recommend_level': item.recommend_level,
                    'uid': item.uid,
                    'update_time': item.update_time,
                    'sort_name': TBlogSort.objects.filter(uid=item.blog_sort_id).values()[0].get('sort_name')
                })

        except Exception as e:
            print(e)
            return JsonResponse({'code': 500, 'msg': 'defeated', })
        return JsonResponse({'code': 1, 'msg': 'success', 'data': result})
