import base64
import random
import re
from datetime import datetime
from io import StringIO
from django.utils.six import BytesIO

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect

# Create your views here.
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from api.models import UserInfo, ConfirmInfo

import traceback
from xlwt import Workbook
from PIL import Image, ImageDraw, ImageFont

# 返回首页
from api.utils.user_util import pass_encryption, make_signed_cookie, hasUser, login_require

from my_website_api.settings import MEDIA_ROOT, MEDIA_URL

# 用户注册
class RegisterView(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        code = request.data.get('code')
        if not name:
            return Response({'success': 0, 'msg': u'注册失败,用户名不能为空'})
        if not email:
            return Response({'success': 0, 'msg': u'注册失败,用户邮箱不能为空'})
        if not password or len(password) < 6:
            return Response({'success': 0, 'msg': u'注册失败,用户密码不能为空并且不能小于6位数'})
        if not code:
            return Response({'success': 0, 'msg': u'注册失败,验证码不能为空!'})

        # 验证码校验
        user_comfirm = ConfirmInfo.objects.filter(email=email, is_success=False).first()
        if not user_comfirm or user_comfirm.code != code:
            return Response({'success': 0, 'msg': u'注册失败,验证码不正确!'})
        # 还要判断验证码是否过期
        time_consume = int(datetime.now().timestamp() - user_comfirm.update_time.timestamp())  # 秒级时间戳
        if time_consume > 30 * 60:
            return Response({'success': 0, 'msg': u'验证码已失效!请重新获取'})

        # 注册账号
        user = UserInfo.objects.filter(name=name)
        if user:
            return Response({'success': 0, 'msg': u'注册失败,用户名已被注册'})
        user_info = UserInfo()
        user_info.name = name
        user_info.email = email
        user_info.password = pass_encryption(password)
        user_info.update_time = datetime.now()
        user_info.save()
        user_comfirm.is_success = True
        user_comfirm.save()
        return Response({'success': 1, 'msg': u'注册成功'})

    # 获取验证码
    def get(self, request):
        email = request.GET.get('user_email')
        if email:
            user = ConfirmInfo.objects.filter(email=email).first()
            if user and user.is_success:
                return Response({'success': 0, 'msg': u'该邮箱已被注册，请使用其他邮箱。'})
            code = self._get_code()
            # 如果发送验证码成功,保存邮箱和验证码信息
            if self._send_email(email, code):
                if user:
                    user.update_time = datetime.now()
                    user.code = code
                    user.save()
                else:
                    ConfirmInfo(code=code, email=email).save()
                return Response({'success': 1, 'msg': u'验证码已发送到你的邮箱，请前往验证'})
            else:
                return Response({'success': 0, 'msg': u'邮箱不正确!'})
        else:
            return Response({'success': 0, 'msg': u'邮箱不能为空'})
    
    def _get_code(self):
        code_list = [str(num) for num in range(0, 10)] + [chr(num) for num in range(65, 91)] + [chr(num) for num in range(97, 123)]
        return "".join(random.sample(code_list, 5))
        
    def _send_email(self, email, code):
        # 在邮件中添加附件的发送方法
        from django.conf import settings
        import smtplib
        from email.mime.text import MIMEText
        from email.utils import formataddr

        ret = True

        try:
            msg = MIMEText("欢迎注册hxc个人网站，您的验证码是%s,请在30分钟内完成注册" % code, 'plain', 'utf-8')
            msg['From'] = formataddr(["huangxiaochang", settings.EMAIL_HOST_USER])
            msg['To'] = formataddr(['hxc', email])
            msg['Subject'] = "注册验证码"
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # SMTP_SSL的默认端口是465
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            # 参数， from， to(列表), mesaage
            server.sendmail(settings.EMAIL_HOST_USER, [email,], msg.as_string())
            # 关闭连接并退出
            server.quit()
        except Exception as e:
            traceback.print_exc()
            ret=False
        return ret

# 用户登录
class LoginView(APIView):
    def post(self, request):
        name = request.data.get('name')
        psd = request.data.get('password')
        code = request.data.get('code')
        if code and code != request.session['captcha_code']:
            return Response({'success': 0, 'msg': u'验证码不正确!'})
        if not name or not psd or not code:
            return Response({'success': 0, 'msg': u'请填写完整登录信息!'})
        else:
            password = pass_encryption(psd)
            # 如果是用filter的话，返回的一个集合，使用get的话，返回的是一个对象
            user = UserInfo.objects.filter(name=name, password=password).first()
        if user:
            # cookie过期的时间
            max_age = 43200
            cookie = make_signed_cookie(user.id, user.password, user.name, max_age)
            response = HttpResponse(json.dumps({"success": 1, 'msg': u'登录成功'}))
            response.set_cookie('user_cookie', cookie, max_age=max_age)  # 向浏览器中设置cookie
            response.set_cookie('user_role', user.role, max_age=max_age)
            response.set_cookie('operate_permission', user.operate_permission, max_age=max_age)
            return response
        else:
            return HttpResponse(json.dumps({'success': 0, 'msg': u'用户名或者密码不正确!'}))

    # 生成图形验证码
    def get(self, request):
        img = Image.new(mode='RGB', size=(100, 30), color=(255, 255, 255))
        draw = ImageDraw.Draw(img, mode='RGB')
        font = ImageFont.truetype("calibri.ttf", 20)
        draw.line((20, 18, 80, 18), fill='red')
        draw.arc((10, 0, 70, 25), 0, 270, fill='green')
        draw.point([50, 15], fill=(0, 0, 0))
        code = ''
        for i in range(4):
            char = random.choice([chr(random.randint(65, 90)), str(random.randint(0, 9))])
            code += char
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            draw.text([i * 25, 12], char, color, font=font)
        request.session['captcha_code'] = code
        # filepath = MEDIA_ROOT + 'captcha.png'
        # file_url = MEDIA_URL + 'captcha.png'
        # with open(filepath, 'wb') as f:
        #     img.save(f, format='png')
        # 以base64的格式返回图形验证码
        del draw
        buf = BytesIO()
        img.save(buf, format='png')
        data = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode(encoding='utf-8')
        return HttpResponse(json.dumps({'url': data}))

# 退出登录
class login_out(APIView):
    def get(self, request):
        user = hasUser(request)
        if user:
            response = HttpResponse(json.dumps({'success': 1, 'msg': u'退出登录成功!'}))
            # response = HttpResponseRedirect('/device_statistic_index/login/')
            response.delete_cookie('user_cookie')
            response.delete_cookie('user_role')
            response.delete_cookie('operate_permission')
            return response
        return Response({'success': 0, 'msg': u'没有此用户'})

@login_require
def get_user_info(request):
    user = hasUser(request)
    if user:
        data = {
            'name': user.name,
            'email': user.email,
            'id': user.id,
            'register_time': str(user.register_time),
            'avatar_url': user.avatar_url,
            'role': user.role,
            'operate_permission': user.operate_permission
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return HttpResponse(json.dumps({'success': 0, 'msg': u'没有此用户'}), content_type="application/json")

# 修改用户信息, 可以拓展成修改其他用户的信息
@login_require
def modify_user_info(request):
    json_data = json.loads(request.body)
    # 如果没有传用户id， 这修改的是当前登录账户的用户名或者密码
    user = hasUser(request)
    if 'user_id' not in json_data or json_data['user_id'] <= 0:
        for key in json_data:
            if key == 'name' and json_data[key] != '':
                other = UserInfo.objects.filter(name=json_data[key]).exclude(id=user.id)
                if other:
                    return HttpResponse(json.dumps({'success': 0, 'msg': u'用户名重复!'}))
                user.name = json_data[key]
            elif key == 'password' and json_data[key] != '':
                if len(json_data[key]) < 6:
                    return HttpResponse(json.dumps({'success': 0, 'msg': u'密码不能为空并且不能小于6位数!'}))
                user.password = pass_encryption(json_data[key])
            elif key == 'email' and json_data[key] != '':
                #  修改绑定的邮箱
                if 'code' not in json_data.keys() or json_data['code'] == '':
                    return HttpResponse(json.dumps({'success': 0, 'msg': u'请输入验证码!'}))
                # 验证码校验
                user_comfirm = ConfirmInfo.objects.filter(email=json_data[key], is_success=False).first()
                if not user_comfirm or user_comfirm.code != json_data['code']:
                    return HttpResponse(json.dumps({'success': 0, 'msg': u'修改失败,验证码不正确!'}))
                user.email = json_data[key]

        user.update_time = datetime.now()
        user.save()
        # 修改用户名和密码之后，要重新登录
        response = HttpResponse(json.dumps({'success': 1, 'msg': u'修改成功!请重新登录'}))
        response.delete_cookie('user_cookie')
        response.delete_cookie('user_role')
        response.delete_cookie('operate_permission')
        return response
    else:
        # 修改的是指定用户的权限
        other = UserInfo.objects.get(id=json_data['user_id'])
        # 只有root或者管理员才有权限修改其他人的权限
        hasPermission = user.role.find('root') >= 0 or user.role.find('admin') >= 0
        if hasPermission == False:
            return HttpResponse(json.dumps({'success': 1, 'msg': u'你没有权限进行此操作!'}))
        # 自己不能修改自己的权限
        if other and other.id != user.id:
        # 接收json类型的post请求的数据，如果是rest_framework框架的话，可以直接使用request.POST进行获取
            for key in json_data:
                if key == 'roles' and isinstance(json_data[key], list):
                    arr = [role for role in json_data[key] if role in ['root', 'admin', 'member']]
                    if len(arr) == 0:
                        arr = ['member']  # 默认为'member
                    # 列表去重
                    arr = list(set(arr))
                    other.role = ','.join(arr)
                elif key == 'operate_permission' and isinstance(json_data[key], list):
                    arr = [per for per in json_data[key] if per in ['add', 'edit', 'del', 'look']]
                    if len(arr) == 0:
                        arr = ['look']  # 默认为'look
                     # 列表去重
                    arr = list(set(arr))
                    other.operate_permission = ','.join(arr)
            other.update_time = datetime.now()
            other.save()
            return HttpResponse(json.dumps({'success': 1, 'msg': u'修改成功!'}))
        return HttpResponse(json.dumps({'success': 0, 'msg': u'没有该用户!'}))

# 上传用户头像
class uploadView(APIView):
    def post(self, request):
        user = hasUser(request)
        if not user:
            return Response({'success': 0, 'msg': u'上传文件失败!没有该用户'})
        file = request.FILES.get('file')
        if file == None:
            return Response({'success': 0, 'msg': u'上传文件不能为空'})
        # 头像存在本地的地址 和 存在数据库中的url
        name = file.name
        type = re.search(r'\.(png|gif|jpeg|jpg)$', name)
        if not type:
            return Response({'success': 0, 'msg': u'上传文件格式不对，只能上传png、gif、jpg格式的图片'})
        file_url = MEDIA_ROOT + user.name + '_' + file.name
        db_url = MEDIA_URL + user.name + '_' + file.name
        with open(file_url, 'wb') as f:
            f.write(file.read())
        user.avatar_url =  db_url
        user.save()
        return Response({'success': 1, 'msg': u'上传文件成功!'})

@login_require
def export_user_info(request):
    if request.method == 'GET':

        user_list = UserInfo.objects.all()
        work_book =  Workbook(encoding='gbk')
        sheet = work_book.add_sheet(u'用户信息表')
        # 表头 row, col, value
        sheet_header = [u'用户名', u'邮箱', u'注册时间', u'角色']
        for j in range(len(sheet_header)):
            sheet.write(0, j, sheet_header[j])

        # 表中的内容
        for i in range(len(user_list)):
            sheet.write(i+1, 0, user_list[i].name)
            sheet.write(i+1, 1, user_list[i].email)
            sheet.write(i+1, 2, str(user_list[i].register_time))
            sheet.write(i+1, 3, user_list[i].role)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=user_info.xls'
        work_book.save(response)
        return response
