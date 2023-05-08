import json

from django.http import JsonResponse
# Create your views here.
from django.views import View

from apps.wxapp.models import WxImgs


class wxGetImgInfo(View):

    def get(self, request, username):
        # 获取微信用户名
        result = WxImgs.objects.filter(username=username)
        data = []
        for item in result:
            data.append({
                'username': item.username,
                'imgurl': item.coverurl,
                'imgstatus': item.imgstatus
            })

        return JsonResponse({'code': 1, 'msg': 'success', 'data': data})

    def post(self, request):

        result = json.loads(request.body)
        url = result.get('url')
        status = result.get('status')
        name = result.get('name')
        try:
            WxImgs.objects.create(username=name,coverurl=url,imgstatus=status)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 0, 'msg': 'err', 'data': 'err'})
        # for item in result:
        #     print(item,'0000000000000000000')
        #     WxImgs.objects.create(username=item.get('name'),coverurl=item.get('url'),imgstatus=item.get('status'))

        print(result)
        return JsonResponse({'code': 1, 'msg': 'success', 'data': result})


class wxChangeInfo(View):
    def post(self,request):

        result = '9'
        return JsonResponse({'code': 1, 'msg': 'success', 'data': result})

