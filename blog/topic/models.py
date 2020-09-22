from django.db import models
from user.models import UserProfile
# Create your models here.

class Topic(models.Model):
    title=models.CharField('文章標題',max_length=50)
    #tec -技術類,no-tec 非技術類
    category=models.CharField('文章分類',max_length=20)
    limit=models.CharField('文章權限',max_length=10)
    introduce=models.CharField('文章簡介',max_length=90)
    content=models.TextField(verbose_name='文章內容')
    create_time=models.DateTimeField(auto_now_add=True)
    modified_time=models.DateTimeField(auto_now=True)
    #外鍵
    author=models.ForeignKey(UserProfile)

    class Meta:
        db_table = 'topic'