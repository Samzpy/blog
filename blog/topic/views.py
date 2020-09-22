from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
import json,datetime,time
from tools.login_check import login_check
from .models import Topic
from user.models import UserProfile
from tools.login_check import get_user_by_request
from message.models import Message

@login_check('POST', 'DELETE')
def topics(request,author_id):
    #127.0.0.1:8000/v1/topics/<author_id>?category=[tec|no-tec]
    if request.method == 'GET':
        #獲取用戶博客數據
        #前端地址 -> http:127.0.0.1:5000/<username>/topics
        #author_id 被訪問的博客的博主用戶名
        #visitor 訪客 1.登入 2.遊客
        authors=UserProfile.objects.filter(username=author_id)
        if not authors:
            result={'code':308,'error':'no author'}
            return JsonResponse(result)
        #取出結果中的博主
        author=authors[0]

        #visitor?
        visitor=get_user_by_request(request)
        visitor_name=None
        if visitor:
            visitor_name=visitor.username
        t_id=request.GET.get('t_id')
        #獲取 t_id
        if t_id:
            #當前是否為博主訪問自己的博客
            is_self=False
            #根據t_id進行查詢
            t_id=int(t_id)
            if author_id==visitor_name:
                is_self=True
                #博主訪問自己
                try:
                    author_topic=Topic.objects.get(id=t_id)
                except Exception as e:
                    result={'code':312,'error':'no topic'}
                    return JsonResponse(result)
            #拼前端返回值
            else:
                #訪客訪問博主的博客
                try:
                    author_topic=Topic.objects.get(id=t_id,limit='public')
                except Exception as e:
                    result={'code':313,'error':'no topic'}
                    return JsonResponse(result)
            res=make_topic_res(author,author_topic,is_self)
            return JsonResponse(res)
            

        else:
            #127.0.0.1:8000/v1/topics/<author_id>?category=[tec|no-tec]

            category=request.GET.get('category')
            if category in ['tec','no-tec']:
                #v1/topics/<author_id>?category=[tec|no-tec]
                if author_id == visitor_name:
                    #博主訪問自己的博客
                    topics=Topic.objects.filter(author_id=author_id,category=category)
                else:
                    #訪客來了
                    topics=Topic.objects.filter(author_id=author_id,category=category,limit='public')

            else:
                #v1/topics/<author_id>
                if author_id==visitor_name:
                    #博主訪問自己的博客 獲取全部數據
                    topics=Topic.objects.filter(author_id=author_id)
                else:
                    #訪客,非博主本人
                    topics =Topic.objects.filter(author_id=author_id,limit='public')
            
            result=make_topics_res(author,topics)
            return JsonResponse(result)
        

        #v1/topics

    elif request.method=="POST":
        json_str=request.body.decode()
        if not json_str:
            result={'code':301,'error':'Please give me json'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        title=json_obj.get('title')
        #xss注入
        import html
        title =html.escape(title)
        if not title:
            result={'code':302,'error':'Please give me title'}
            return JsonResponse(result)
        content=json_obj.get('content')
        if not content:
            result={'code':303,'error':'Please give me content'}
            return JsonResponse(result)
        content_text=json_obj.get('content_text')
        if not content_text:
            result={'code':304,'error':'Please give me content_text'}
            return JsonResponse(result)
        introduce=content_text[:30]
        limit=json_obj.get('limit')
        if limit not in ['public','private']:
            result={'code':305,'error':'Please give me limit'}
            return JsonResponse(result)
        category = json_obj.get('category')
        #TODO 檢查 sam to 'limit'
        #創建數據
        Topic.objects.create(title=title,category=category,limit=limit,content=content,introduce=introduce,author=request.user)
        result={'code':200,'username':request.user.username}
        return JsonResponse(result)

    elif request.method == 'DELETE':
        #博主删除自己的文章
        #/v1/topics/<author_id>
        # token存储的用户
        author = request.user
        token_author_id = author.username
        #url中传过来的author_id 必须与token中的用户名相等
        if author_id != token_author_id:
            result = {'code':309, 'error': 'You can not do it '}
            return JsonResponse(result)

        topic_id = request.GET.get('topic_id')

        try:
            topic = Topic.objects.get(id=topic_id)
        except:
            result = {'code':310, 'error': 'You can not do it !'}
            return JsonResponse(result)

         #删除
        if topic.author.username != author_id:
            result = {'code': 311, 'error': 'You can not do it !! '}
            return JsonResponse(result)

        topic.delete()
        res = {'code':200}
        return JsonResponse(res)
@login_check('PUT')
def modify(request,username=None,tid=None):
    print("*"*70) 
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
                result = {'code':208,'error':'no user'}
                return JsonResponse(result)
            try:
                topic=Topic.objects.get(id=tid)
            except Exception as e:
                result = {'code':208,'error':'no content'}
                return JsonResponse(result)

            #全量查詢[password email 不給]
            result ={'code':200,'username':username,'data':{'info':user.info,'sign':user.sign,'avatar':str(user.avator),'nickname':user.nickname,'title':topic.title,'content':topic.content}}
            return JsonResponse(result)   
    elif request.method=="PUT":
        json_str=request.body.decode()
        if not json_str:
            result={'code':301,'error':'Please give me json'}
            return JsonResponse(result)
        json_obj=json.loads(json_str)
        title=json_obj.get('title')
        #xss注入
        import html
        title =html.escape(title)
        if not title:
            result={'code':302,'error':'Please give me title'}
            return JsonResponse(result)
        content=json_obj.get('content')
        if not content:
            result={'code':303,'error':'Please give me content'}
            return JsonResponse(result)
        content_text=json_obj.get('content_text')
        if not content_text:
            result={'code':304,'error':'Please give me content_text'}
            return JsonResponse(result)
        introduce=content_text[:30]
        limit=json_obj.get('limit')
        if limit not in ['public','private']:
            result={'code':305,'error':'Please give me limit'}
            return JsonResponse(result)
        category = json_obj.get('category')
        #TODO 檢查 sam to 'limit'
        #創建數據
        # Topic.objects.create(title=title,category=category,limit=limit,content=content,introduce=introduce,author=request.user)
        modify_topic=Topic.objects.get(id=tid)
        modify_topic.title=title
        modify_topic.category=category
        modify_topic.limit=limit
        modify_topic.content=content
        modify_topic.introduce=introduce
        modify_topic.author=request.user
        modify_topic.save()
        result={'code':200,'username':request.user.username}
        return JsonResponse(result)


def make_topics_res(author, topics):
    res = {'code':200 , 'data':{}}
    data = {}
    data['nickname'] = author.nickname
    topics_list = []
    for topic in topics:
        d = {}
        d['id'] = topic.id
        d['title'] = topic.title
        d['category'] = topic.category
        d['introduce'] = topic.introduce
        d['author'] = author.nickname
        d['created_time'] = topic.create_time.strftime('%Y-%m-%d %H:%M:%S')
        topics_list.append(d)
    topics_list.reverse()

    data['topics'] = topics_list
    res['data'] = data
    return res

def make_topic_res(author,author_topic,is_self):

    if is_self:
        #博主訪問自己博客
        #下一篇文章:取出ID大於當前博客ID的第一個且author 為當前作者
        last_topic = Topic.objects.filter(id__gt=author_topic.id,author_id=author).first()

        #上一篇文章:取出ID小於當前博客ID的最後一個且author 為當前作者
        next_topic = Topic.objects.filter(id__lt=author_topic.id,author_id=author).last()

    else:
        #訪客訪問博主的
        #下一篇
        last_topic = Topic.objects.filter(id__gt=author_topic.id,author_id=author.username,limit='public').first()

        #上一篇
        next_topic = Topic.objects.filter(id__lt=author_topic.id,author_id=author.username,limit='public').last()

    if next_topic:
        next_id=next_topic.id
        next_title=next_topic.title
    else:
        next_id=None
        next_title=None
    if last_topic:
        last_id=last_topic.id
        last_title=last_topic.title
    else:
        last_id=None
        last_title=None

  
    all_messages=Message.objects.filter(topic=author_topic).order_by("-created_time")
    #所有的留言
    msg_list=[]
    msg_count=0
    #留言和回覆的映射字典
    reply_dict={}
    for msg in all_messages:
        msg_count+=1
        if msg.parent_message == 0:
            #當前0是留言
            msg_list.append({'id':msg.id,'content':msg.content,'publisher':msg.publisher.nickname,
            'publisher_avatar':str(msg.publisher.avator),
            'created_time':msg.created_time.strftime('%Y-%m-%d'),'reply':[]})
        else:
            #當前是回覆
            reply_dict.setdefault(msg.parent_message,[])
            reply_dict[msg.parent_message].append({'msg_id':msg.id,'content':msg.content,'publisher':msg.publisher.nickname,
            'publisher_avatar':str(msg.publisher.avator),
            'created_time':msg.created_time.strftime('%Y-%m-%d')})
    

    #合併msg_list 和reply_dict
    for _msg in msg_list:
        if _msg['id'] in reply_dict:
            _msg['reply']=reply_dict[_msg['id']]   







    res = {'code':200, 'data':{}}
    res['data']['nickname'] = author.nickname
    res['data']['title'] = author_topic.title
    res['data']['category'] = author_topic.category
    res['data']['created_time'] = author_topic.create_time.strftime('%Y-%m-%d %H:%M:%S')
    res['data']['content'] = author_topic.content
    res['data']['introduce'] = author_topic.introduce
    res['data']['author'] = author.nickname
    res['data']['next_id'] = next_id
    res['data']['next_title'] = next_title
    res['data']['last_id'] = last_id
    res['data']['last_title'] = last_title
    #messages 暂时为假数据
    res['data']['messages'] = msg_list
    res['data']['messages_count'] = msg_count
    return res



    

