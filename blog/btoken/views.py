from django.shortcuts import render
from django.http import JsonResponse
import json,hashlib,time,jwt
# Create your views here.
from user.models import UserProfile
def tokens(request):
    if not request.method =='POST':
        result={'code':101,'error':'Please use POST'}
        return JsonResponse(result)
    #前端地址 https://127.0.0.1:5000/login
    #獲取前端傳來的數據/生成token
    #獲取-效驗密碼-生成token
    json_str=request.body.decode()
    if not json_str:
        result={'code':102,'error':'Please me json'}
        return JsonResponse(result)
    json_obj=json.loads(json_str)
    username=json_obj.get('username')
    if not username:
        result={'code':103,'error':'Please me username'}
        return JsonResponse(result)
    password=json_obj.get('password')
    if not password:
        result={'code':104,'error':'Please me password'}
        return JsonResponse(result)

    #效驗數據====
    user=UserProfile.objects.filter(username=username)
    if not user:
        #故意說用戶或密碼錯 防止有心人士
        result = {'code':105,'error':'username or password is wrong!!'}

    user=user[0]
    m=hashlib.md5()
    m.update(password.encode())
    if m.hexdigest()!=user.password:
        result = {'code':106,'error':'username or password is wrong'}
        return JsonResponse(result)
    #make token
    token=make_token(username)
    result={'code':200,'username':username,'data':{'token':token.decode()}}
    print(result)
    return JsonResponse(result)


def make_token(username,expire=3600*24):
    key='1234567'
    now=time.time()
    payload={'username':username,'exp':int(now+expire)}

    return jwt.encode(payload,key,algorithm='HS256')