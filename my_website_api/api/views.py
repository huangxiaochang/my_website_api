import random
from datetime import datetime

from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserInfo, ConfirmInfo


# 返回首页
def index(request):
    return render_to_response('index.html')

# 用户注册
class RegisterView(APIView):
    def post(self, request):
        # if request.session.get('is_login', None):
        #     return redirect('/')
        name = request.data.get('account_name')
        email = request.data.get('user_email')
        password = request.data.get('password')
        code = request.data.get('verification_code')
        if name and email and password:
            # 验证码校验
            if not code:
                return Response({'success': 0, 'msg': u'注册失败,验证码不能为空!'})
            user = ConfirmInfo.objects.filter(email=email).first()
            if not user or user.code != code:
                return Response({'success': 0, 'msg': u'注册失败,验证码不正确!'})
            
            # 注册账号
            users = UserInfo.objects.all()
            if users.filter(email=email):
                return Response({'success': 0, 'msg': u'注册失败,邮箱已被注册'})
            elif users.filter(name=name):
                return Response({'success': 0, 'msg': u'注册失败,用户名已被注册'})
            else:
                user_info = UserInfo()
                user_info.name = name
                user_info.email = email
                user_info.password = password
                user_info.save()
                return Response({'success': 1, 'msg': u'注册成功'})
        else:
            return Response({'success': 0, 'msg': u'注册失败,用户信息不全'})
        
    def get(self, request):
        email = request.GET.get('email')
        if email:
            code = self._get_code()
            user = ConfirmInfo.objects.filter(email=email).first()
            if user:
                user.code = code
            else:
                user = ConfirmInfo()
                user.email = email
                user.code = code
                user.add_time = datetime.now()
            self._send_email(email, code)
            user.save()
            return Response({'success': 1, 'msg': u'验证码已发送到你的邮箱，请前往验证', 'data': code})
        else:
            return Response({'success': 0, 'msg': u'邮箱不能为空'})
    
    def _get_code(self):
        code_list = [str(num) for num in range(0, 10)] + [chr(num) for num in range(65, 91)] + [chr(num) for num in range(97, 123)]
        return "".join(random.sample(code_list, 5))
        
    def _send_email(self, email, code):
        # 在邮件中添加附件的发送方法
        from django.conf import settings
        # from django.core.mail import EmailMultiAlternatives
        from django.core.mail import send_mail
        subject = '来自10.249.30.112:8000的注册确认邮件'
        
        text_content = '感谢您注册hxc的个人网站，请放心，此完整只是用于学习，不会进行用户信息的手机, 您的验证码是{}'.format(code)
        
        html_content = '''
                        <p>您的验证码是{}</p>
                        <p>有效期为24小时，请尽快完成验证,谢谢!</p>
                        '''.format(code)
        send_mail(subject, text_content, settings.EMAIL_HOST_USER, [email])
        # msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()