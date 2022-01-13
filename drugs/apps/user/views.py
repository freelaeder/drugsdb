from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class UserInfoView(View):
    def get(self, request):
        print('ok')

        return JsonResponse({'code': 1, 'errmsg': 'ok'})
