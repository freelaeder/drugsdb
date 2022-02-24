from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class ImageCodeView(View):
    def get(self, request):
        # 获取前段发送的uuid
        uuid = request.GET.get('uuid')
        # 调用产生图形验证码
        from libs.captcha.captcha import captcha
        # text 是图形验证码的内容
        # images 是图片的二进制
        text, images = captcha.generate_captcha()
        # 通过redis 连接保存 uuid和 text，并返回images
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')
        # 保存uuid
        redis_cli.setex(uuid, 300, text)
        print(uuid, text, '--------------')
        # 返回图形验证码
        return HttpResponse(images, content_type='image/jpeg')


class ImageCodeInfoView(View):
    def get(self, request):
        # 获取前端发送的数据
        # 图形验证码
        text: str = request.GET.get('utext')
        # uuid
        uuid = request.GET.get('uuid')
        # 手机号
        mobile = request.GET.get('mobile')
        print(text, uuid)
        # 验证参数是否齐全
        if not all([text, uuid, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '貌似少了东西呦'})
        # 连接redis
        from django_redis import get_redis_connection

        try:
            redis_cli = get_redis_connection('code')
            # 获取redis存的uuid
            redis_text: str = redis_cli.get(uuid)
            if redis_text is None:
                return JsonResponse({'code': 400, 'errmsg': '您输入的图片验证码已过期呦'})
            # 解码
            redis_text = redis_text.decode()
            # 比较
            if text.lower() != redis_text.lower():
                return JsonResponse({'code': 400, 'errmsg': '您输入的不对呦'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '请稍后试试'})
        # 发送短信验证码
        # 设置手机号，防止短时间内多次发送
        flag_send = redis_cli.get('flag_%s' % mobile)
        # 如果存在，退出执行
        if flag_send:
            return JsonResponse({'code': 400, 'errmsg': '您的手机号已经发送了'})
        # 生产随机的短信验证码
        from random import randint
        sms_code = '%06d' % randint(0, 999999)
        print('随机的验证码', sms_code)
        # 创建redis 管道 pipline 对象
        pl = redis_cli.pipeline()
        # 保存随机的短信验证码
        pl.setex(mobile, 300, sms_code)
        # 保存 手机号
        pl.setex('flag_%s' % mobile, 60, 1)
        # 请求执行
        pl.execute()
        print(flag_send, 'flag_send')
        # 调用发送短信的任务
        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile=mobile, code=sms_code)
        # 最终返回
        return JsonResponse({'code': 1, 'errmsg': 'ok', 'text': text})
