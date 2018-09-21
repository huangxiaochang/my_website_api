import random
from datetime import datetime

from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.http import HttpResponse
from django.template.response import TemplateResponse
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from .models import UserInfo, ConfirmInfo
import traceback

# 返回首页index.html
def index(request):
    print(12212)
    # return TemplateResponse(request, 'index.html', {'name': 'hxc'})
    return render_to_response('index.html', {'name': 'hxc'})
    # return HttpResponse('hello word')

def page_not_found(request, arg = None):
    response = render(request, 'index.html', {'name': json.dumps({'name': 'hxc'})})
    # response = render_to_response('index.html')
    return response
