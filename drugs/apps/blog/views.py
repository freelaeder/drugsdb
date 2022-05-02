import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
# 连接数据库
from pymysql import connect


# 获取列表详情页
class ShowArticleList(View):
    def post(self, request):
        data_dict = json.loads(request.body)
        print(data_dict)
        # {'blogStatus': 1, 'currentPage': 1, 'pageSize': 20}
        blogStatus = data_dict.get('blogStatus')
        currentPage = data_dict.get('currentPage')
        pageSize = data_dict.get('pageSize')
        # 创建Connection连接
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
                f'select d.uid,d.blog_title,d.blog_summary,d.blog_content,d.create_time,s.sort_name from t_blog as d left join t_blog_sort as s on d.blog_sort_id = s.uid order by d.clicks desc limit {pageSize * (currentPage - 1)},{(pageSize * (currentPage - 1)) + 20}')
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
                }
                result.append(result_data)
                # result[i]['blog_sort_id'] = blog_list[i][0]
                # result[i]['blog_title'] = blog_list[i][1]
                # result[i]['blog_summary'] = blog_list[i][2]
                # result[i]['blog_content'] = blog_list[i][3]
                # result[i]['create_time'] = blog_list[i][4]
            # 拼接数据返回
            data = {
                'currentPage': currentPage,
                'pageSize': pageSize,
                'total': 61,
                'result': result,
            }
        except Exception as e:
            print(e)
            return JsonResponse({'code': 405, 'msg': 'err', 'data': data})

        return JsonResponse({'code': 1, 'msg': 'ok', 'data': data})
