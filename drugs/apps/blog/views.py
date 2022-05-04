import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
# 连接数据库
from pymysql import connect

# 获取列表详情页
from apps.blog.models import TBlog, TBlogSort, MtBlogBlogTag, TBlogTag


class ShowArticleList(View):
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
        # 请求sql
        # select d.uid,d.blog_title,d.blog_summary,d.blog_author_id,s.sort_name,d.clicks,d.blog_content,d.create_time from t_blog as d left join t_blog_sort as s on d.blog_sort_id = s.uid order by clicks desc limit 0, 20;
        # select d.uid,d.blog_title,d.blog_summary,blog_content,d.create_time,s.sort_named from t_blog as d left join t_blog_sort as s on d.blog_sort_id = s.uid order by clicks desc limit 0, 20;
        # 判断是第几次请求
        # if currentPage == 1:
        #     blog_data = cs1.execute(
        #         f'select d.uid,d.blog_title,d.blog_summary,d.blog_content,d.create_time,s.sort_name from t_blog as d left join t_blog_sort as s on d.blog_sort_id = s.uid order by d.clicks desc limit 0,{pageSize}')
        # else:
        #     blog_data = cs1.execute(
        #         f'select d.uid,d.blog_title,d.blog_summary,d.blog_content,d.create_time,s.sort_name from t_blog as d left join t_blog_sort as s on d.blog_sort_id = s.uid order by d.clicks desc limit {pageSize * (currentPage - 1)},{(pageSize * (currentPage - 1)) + 20}')
        try:
            blog_data = cs1.execute(
                f'select d.uid,d.blog_title,d.blog_summary,d.blog_content,d.create_time,s.sort_name,d.cover_url from t_blog as d left join t_blog_sort as s on d.blog_sort_id = s.uid order by d.clicks desc limit {pageSize * (currentPage - 1)},{(pageSize * (currentPage - 1)) + 10}')
            # 打印获取的行数
            # print(blog_data)
            # 获取全部
            als = cs1.fetchall()
            print(type(als))
            # 转化为数组
            blog_list = list(als)
            # print(blog_list[20][0])
            result = []
            # 遍历要根据获取的数组长度遍历，不能根据pageSize ，万一没有数据，该程序报错
            for i in range(len(als)):
                result_data = {
                    'blog_sort_id': blog_list[i][0],
                    'blog_title': blog_list[i][1],
                    'blog_summary': blog_list[i][2],
                    'blog_content': blog_list[i][3],
                    'create_time': blog_list[i][4],
                    'sort_name': blog_list[i][5],
                    'cover_url': blog_list[i][6],
                    'uid': blog_list[i][0],
                }
                result.append(result_data)
                # result[i]['blog_sort_id'] = blog_list[i][0]
                # result[i]['blog_title'] = blog_list[i][1]
                # result[i]['blog_summary'] = blog_list[i][2]
                # result[i]['blog_content'] = blog_list[i][3]
                # result[i]['create_time'] = blog_list[i][4]
            # 拼接数据返回
            # 获取blog的总数
            blog_num = TBlog.objects.count()
            print(blog_num)
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
            print(type(uid))
            # 获取sort_id 以下两种都可以
            # 获取 sort_name
            sort_id = TBlog.objects.filter(uid=uid).values('blog_sort_id').values()[0].get('blog_sort_id')
            # sort_id = TBlog.objects.get(uid=uid)
            # print(sort_id.blog_sort_id)

            sort_name = TBlogSort.objects.get(uid=sort_id)
            # 获取 sort_name
            sort_name = sort_name.sort_name
            print(sort_name)
            # 获取tag
            tag_id = MtBlogBlogTag.objects.filter(blog_id=uid)
            # 假如有多个先储存起来，再一一获取tag名字
            tag_list = []
            # 定义返回的列表
            blog_tags = []
            for item in tag_id:
                blog_tags.append({
                    'blog_tag_id': item.blog_tag_id,
                    'tag_name': TBlogTag.objects.filter(uid=item.blog_tag_id).values()[0].get('tag_name'),
                })
                # tag_list.append(item.blog_tag_id)
                # print(TBlogTag.objects.filter(uid=item.blog_tag_id).values()[0].get('tag_name'))
            print(tag_list)

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
        return JsonResponse({'code': 1, 'msg': 'succes', 'data': result})
