from django.shortcuts import render, render_to_response


# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserInfo


def index(request):
    return render_to_response('index.html')

class RegisterView(APIView):
    def post(self, request):
        account_name = request.data.get('account_name')
        user_emit = request.data.get('user_emit')
        password = request.data.get('password')
        print(account_name)
        print(user_emit)
        print(password)
        if account_name and user_emit and password:
            user_info = UserInfo()
            user_info.account_name = account_name
            user_info.user_emit = user_emit
            user_info.password = password
            # user_info.save()
            return Response({'success': 1, 'msg': u'注册成'})
        else:
            return Response({'success': 0, 'msg': u'注册失败,用户信息不全'})