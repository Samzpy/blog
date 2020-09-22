from django.db import models

# Create your models here.

class UserProfile(models.Model):

    username=models.CharField('用戶姓名',max_length=11,primary_key=True)

    nickname=models.CharField('綽號',max_length=30)

    email = models.CharField('信箱',max_length=50,null=True)

    password=models.CharField(max_length=32)

    sign=models.CharField('狀態消息',max_length=50)

    info=models.CharField('自我介紹',max_length=150)

    avator=models.ImageField(upload_to='avatar/')
    
    #更改數據名稱
    class Meta:
        db_table='user_profile'
