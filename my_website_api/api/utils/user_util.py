# 使用md5对密码进行加密
import time
import hashlib

from api.models import UserInfo
from django.http import HttpResponse
from rest_framework.utils import json


def pass_encryption(password):
    m = hashlib.md5(password.encode(encoding='utf-8'))
    return m.hexdigest()

# 计算加密cookie
def make_signed_cookie(id, password, name, max_age):
    expires = str(int(time.time() + max_age))
    cookie = [str(id), expires, hashlib.md5(('%s-%s-%s-%s' % (id, password, name, 'user_cookie')).encode(encoding='utf-8')).hexdigest()]
    return ';'.join(cookie)

# 获取用户cookie,判断是否有该用户
def hasUser(rq):
    user_cookie = rq.COOKIES.get('user_cookie')
    if user_cookie == None:
        return {}
    info_list = user_cookie.split(';')
    user = UserInfo.objects.filter(id=int(info_list[0])).first()
    ck = hashlib.md5(
        ('%s-%s-%s-%s' % (user.id, user.password, user.name, 'user_cookie')).encode(encoding='utf-8')).hexdigest()
    if ck == info_list[2]:
        return user
    return {}

def login_require(fun):
    def decorator_wrap(request, *args, **kwargs):
        user_cookie = request.COOKIES.get('user_cookie')
        if not user_cookie:
            return HttpResponse(json.dumps({'success': 0, 'msg': u'用户没有登录!'}))
        return fun(request, *args, **kwargs)
    return decorator_wrap
