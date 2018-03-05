#_*_ encoding:UTF-8 _*_

from __future__ import unicode_literals                 #python的import区域，每个区域隔一行
from datetime import datetime

from django.db import models                            #第三方（如djiano）的import区域
from django.contrib.auth.models import AbstractUser

# Create your models here.

#models  数据表设计，设计与数据库有关的


class UserProfile(AbstractUser):                #在已有的字段中，添加一些需要使用的字段
    nick_name = models.CharField(max_length=50,verbose_name=u"昵称",default=" ")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6,choices=(("male",u"男"),("female",u"女")), default = "female")
    address = models.CharField(max_length=100,default=u"")
    mobile = models.CharField(max_length=11,null=True,blank=True)
    image = models.ImageField(upload_to ="image/%Y/%m",default=u"image/default.png",max_length=100)

    class Meta:
        verbose_name = "用户信息"           #model名称，列表名
        verbose_name_plural = verbose_name    #去掉一个s

    def __unicode__(self):          #显示string,对象名字
        return self.username


class  EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u"验证码")
    email = models.EmailField(max_length=50,verbose_name=u"邮箱")
    send_type = models.CharField(choices=(("register",u"注册"),("forget",u"找回密码")),max_length=10,verbose_name=u"验证码类型")
    send_time = models.DateTimeField(default=datetime.now,verbose_name=u"发送时间")    #now去掉括号为实例化时的时间，不然为创建model编译的时间

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code,self.email)

class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m",verbose_name=u"轮播图",max_length=100)   #数据库存储的是图片的路径地址
    url = models.URLField(max_length=200,verbose_name=u"访问地址")
    index = models.IntegerField(default=100,verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name