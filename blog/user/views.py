from django.shortcuts import render
from django.http import JsonResponse
import jwt
import json,time,hashlib
from .models import *
from tools.login_check import login_check

# from btoken.views import make_token
# Create your views here.
@login_check('PUT')
def users(request,username=None):
    if request.method == "GET":
        #獲取用戶數據
        if username:
            #/v1/users/<username>
            #拿指定用戶數據
            #/v1/users/<username>?nickname=1
            #拿指定用戶的指定字段數據
            try:
                user=UserProfile.objects.get(username=username)
            except Exception as e:
                user=None
                if not user:
                    result = {'code':208,'error':'no user'}
                return JsonResponse(result)
            #檢查是否有查詢字符串
            if request.GET.keys():
                #查詢指定字段
                data={}
                for k in request.GET.keys():
                    if hasattr(user,k):
                        v=getattr(user,k)
                        if k == 'avator':
                            data[k]=str(v)
                        if k =='password':
                            continue
                        data[k]=v
                result={'code':200,'username':username,'data':data}
                return JsonResponse(result)
            else:
                #全量查詢[password wmail 不給]
                result ={'code':200,'username':username,'data':{'info':user.info,'sign':user.sign,'avatar':str(user.avator),'nickname':user.nickname}}
                return JsonResponse(result)
    elif request.method=='POST':
        #創建用戶
        #前端註冊頁面地址 http://127.0.0.1:5000/register
        #{‘username’: jack, ‘email’: ‘abc@qq.com’, ‘password1’: ‘abcdef’,‘password2’: ‘abcdef’}
        json_str=request.body.decode()
        json_obj=json.loads(json_str)
        username=json_obj.get('username','')
        email=json_obj.get('email','')
        password1=json_obj.get('password_1','')
        password2=json_obj.get('password_2','')
        if not json_str:
            return JsonResponse({'code':205,'error':'no data'})
        if username =="" and len(username) <6:
            return JsonResponse({'code':201,'error':'用戶名長度須大於6'})
        if email =="" and '@'not in email:
            return JsonResponse({'code':202,'error':'尚未填寫信箱 或 格式錯誤'})
        if password1 =="" and len(password1)<6:
            return JsonResponse({'code':203,'error':'尚未填寫密碼一或長度小於6'})
        if password2 =="" and len(password2)<6:
            return JsonResponse({'code':204,'error':'尚未填寫密碼二或長度小於6'})
        if password1 != password2:
            return JsonResponse({'code':204,'error':'重複密碼須相同'})
        #優先查詢當前用戶名是否存在
        old_user=UserProfile.objects.filter(username=username)
        #filter 返回集合 找不到空   get找不到則報做 返回單元訴
        if old_user:
            result ={'code':206,'error':'Your username is already exist'}
            return JsonResponse(result)
        #密碼處理 md5哈西/散列
        m=hashlib.md5()
        m.update(password1.encode())
        #==========charfield 盡量避免使用 null=True
        sign=info=''
        try:
            UserProfile.objects.create(username=username,nickname=username,password=m.hexdigest(),sign=sign,info=info,email=email)
        #用戶名重複 或 數據庫down
        except Exception as e:
            result={'code':207,'error':'Sever is busy'}
            return JsonResponse(result)

        #make token
        token=make_token(username)
        #正常返回前端
        result={'code':200,'username':username,'data':{'token':token.decode()}}
        return JsonResponse(result)

    elif request.method=="PUT":
        #http://127.0.0:5000/<username>/change_info
        #更新數據
        #此頭可獲取前端傳來的tiken
        #META可拿去http協議原生頭,META也是類字典對想可以使用字典相關方法
        #特別注意http頭有可能被django重命名,建議百度
        user=request.user
        json_str=request.body.decode()
        if not json_str:
            result = {'code':209,'error':'Please give me json'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        if 'sign' not in json_obj:
            result ={'code':210,'error':'no sign'}
            return JsonResponse(result)
        if 'info' not in json_obj:
            result ={'code':210,'error':'no info'}
            return JsonResponse(result)
        sign=json_obj.get('sign','')
        info=json_obj.get('info','')
        request.user.sign=sign
        request.user.info=info
        request.user.save()
        result={'code':200,'username':request.user.username}
        return JsonResponse(result)
        

    else:
        raise


#將token方法(user) 移出 怕重複代碼)
def make_token(username,expire=3600*24):
    key='1234567'
    now=time.time()
    payload={'username':username,'exp':int(now+expire)}

    return jwt.encode(payload,key,algorithm='HS256')

@login_check('POST')
def users_avatar(request,username):
    if request.method !='POST':
        result={'code':212,'error':'I need post'}
        return JsonResponse(result)
    avatar=request.FILES.get('avatar','')
    if not avatar:
        result={'code':213,'error':'I need avatar'}

    #TODO 判定url中的username 是否跟 token 中的username是否一直 若否則返回error
    request.user.avator=avatar
    request.user.save()
    result = {'code':200,'username':request.user.username}
    print(123)
    print(result)
    return JsonResponse(result)