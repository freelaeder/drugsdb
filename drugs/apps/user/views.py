import json
import re
import time

from django.contrib.auth import login, authenticate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
# 导入user models.py
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.user.models import *

# 验证用户名
from apps.user.serializers import UserSerializers


class UserInfoView(View):
    def get(self, request):
        # 接受username
        username = request.GET.get('username')
        # 连接数据库
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({'code': 0, 'errmsg': 'err'})
        # 返回参数count
        return JsonResponse({'code': 1, 'errmsg': 'ok', 'count': count})


# 验证手机号
class PhoneInfoView(View):
    def get(self, request):
        # 获取手机号
        phone = request.GET.get('uphone')
        print(phone)
        # 验证手机号在数据库中是否已经存在
        try:
            count = User.objects.filter(mobile=phone).count()
        except Exception as e:
            return JsonResponse({'code': 0, 'errmsg': 'err'})

        return JsonResponse({'code': 1, 'errmsg': 'ok', 'count': count})


# 用户注册
class RegisterView(View):
    def post(self, request):
        # 获取前端传递的数据
        body_byte = request.body
        data_dict = json.loads(body_byte)
        print(data_dict)
        # {'username': 'free', 'password': 'free',
        # 'password2': 'free', 'mobile': '18916216440',
        # 'sms_code': '925826'}
        username = data_dict.get('username')
        password = data_dict.get('password')
        password2 = data_dict.get('password2')
        mobile = data_dict.get('mobile')
        sms_code = data_dict.get('sms_code')
        # 验证参数是否齐全
        if not all([username, password, password2, mobile, sms_code]):
            return JsonResponse({'code': 400, 'errmsg': '传递的参数少了呦'})
        # 后端再次验证参数
        # 判断用户名是否是2-5个字符
        # if not re.match(r'^[a-zA-Z0-9_]{1,5}$', username):
        #     return JsonResponse({'code': 400, 'errmsg': 'username格式有误!'})
        # 判断密码是否是2-20个数字
        if not re.match(r'^[0-9A-Za-z]{2,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})
        # 判断两次密码是否一致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})
        # 获取redis中的 短信
        try:
            from django_redis import get_redis_connection
            redis_cli = get_redis_connection('code')
            # 获取短信验证码
            redis_sms_code: str = redis_cli.get(mobile)
            print(f'redis中的验证码{redis_sms_code}')
            # 如果找不到证明验证码已过期
            if not redis_sms_code:
                return JsonResponse({'code': 400, 'errmsg': '您输入的短信验证码已过期呦'})
            # 解码
            redis_sms_code = redis_sms_code.decode()
            print(f'解码后{redis_sms_code}')
            # 如果不等于返回
            if sms_code != redis_sms_code:
                return JsonResponse({'code': 400, 'errmsg': '您输入的短信验证码不对呦'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '连接失败请稍后试试'})

        # 保存数据
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '服务器跑丢了呢'})
        # 状态保持
        login(request, user)
        # 注册时，用户名写到cookie，有效期15天
        response = JsonResponse({'code': 1, 'errmsg': '您已成功注册，正在跳转新世界'})
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        return response


# 用户登录
class LoginView(View):

    def post(self, request):
        # 1 接收json数据
        body = request.body
        data_dict = json.loads(body)
        username = data_dict.get('username')
        password = data_dict.get('password')
        remembered = data_dict.get('remembered')
        # 2 验证数据是否为空  正则
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必要参数呦'})

        import re
        # 验证用户登录方式 手机 账号
        if re.match('^1[3-9]\d{9}$', username):
            # 手机号
            User.USERNAME_FIELD = 'mobile'
        else:
            # account 是用户名
            # 根据用户名从数据库获取 user 对象返回.
            User.USERNAME_FIELD = 'username'

        # 3 验证码用户名和密码是否正确
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({'code': 400, 'errmsg': '用户名密码错误呦'})
        print(user)
        # 4 状态保持
        login(request, user)

        # 5 判断是否记住登录
        if remembered:
            # 如果记住:  设置为两周有效
            request.session.set_expiry(None)
        else:
            # 如果没有记住: 关闭立刻失效
            request.session.set_expiry(0)
        # 6 返回响应
        # 注册时用户名写入到cookie，有效期15天
        response = JsonResponse({'code': 1, 'errmsg': 'ok', 'username': user.username})
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        return response


# 保存用户基本信息
class SaveInfo(View):
    # 更新数据
    def post(self, request):
        # 获取参数
        data_dict = json.loads(request.body)
        print(data_dict)
        # {'username': '12', 'sex': '0', 'email': 'yanglo67@qq.com', 'desc': '123', 'tecs': ['html', 'css', 'celery']}
        username = data_dict.get('username')
        # 旧的名字
        oldusername = data_dict.get('oldusername')
        sex = data_dict.get('sex')
        email = data_dict.get('email')
        desc = data_dict.get('desc')
        tecs = data_dict.get('tecs')
        print(f'tecs{tecs}')
        school = data_dict.get('school')
        # 验证参数
        if not all([username, sex, email, desc, oldusername, school]):
            return JsonResponse({'code': 0, 'errmsg': '参数不够'})
        # 连接数据库更新数据
        try:
            user = User.objects.filter(username=oldusername).update(gender=sex, email=email, description=desc,
                                                                    username=username, tecs=tecs, school=school)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 0, 'errmsg': '数据库更新失败'})

        return JsonResponse({'code': 1, 'errmsg': 'ok', 'user': user})


# 获取用户信息
class UserSaveModel(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    lookup_field = 'username'


class SaveImg(APIView):
    def post(self, request):
        # <MultiValueDict: {'file': [<InMemoryUploadedFile: Group.png (image/png)>]}>
        # 获取图片
        img = request.FILES.get('file')
        # 获取用户名
        user = request.data.get('username')
        file_name = './static/img/' + str(int(time.time())) + '.' + img.name.split('.')[-1]  # 构造文件名以及文件路径
        print(file_name[1:])
        # if img.name.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
        #     return HttpResponse('输入文件有误')
        try:
            with open(file_name, 'wb+') as f:
                f.write(img.read())
            # 更新图片地址
            # 拼接url
            imgurl = 'http://192.168.232.128:8300' + file_name[1:]
            print(imgurl)
            User.objects.filter(username=user).update(default_image=imgurl)
        except Exception as e:
            print(e)
        return JsonResponse({'code': 1, 'errmsg': 'ok', 'default_img': imgurl, 'message': '您已上传成功，快去看看吧'})
