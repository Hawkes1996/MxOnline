# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q                                  #实现并集
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password                   #用户的函数auth

from .models import UserProfile,EmailVerifyRecord
from forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm    #表单的定义
from utils.email_send import send_register_email   #发送邮件的app下的函数


#  自定义认证方法
# Create your views here.


class CustomBackend(ModelBackend):  #实现邮箱和用户名登录
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))    #并集的查询，登录的时候可以使用email登录
            if user.check_password(password):          #密码为密文用check方法进行匹对
                return user
        except Exception as e:
            return None


class LoginView(View):   #登录逻辑
    def get(self,request):
        return render(request, "login.html", {})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")       #从页面取回username(实例化一个user_name)
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)  # 认证方法
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html", {})
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!"})   #这个为form验证完后，在后台验证用户名和密码为错误
        else:
            return render(request, "login.html", {"login_form":login_form})   #这个为form验证的时候显示错误信息，还没在后台数据进行验证


class AciveUserView(View):    #判断是否激活账号，并直接返回登录进行登录
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request,"active_fail.html")  #验证失败的判断
        return render(request, "login.html")


class RegisterView(View):   #注册逻辑
    def get(self,request):                      #get从服务器获得数据
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form':register_form})
    def post(self,request):                     #post向服务器传送数据
        register_form = RegisterForm(request.POST)          #request初始化form
        if register_form.is_valid():
            user_name = request.POST.get("email", "")       #取出email
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form,"msg":"用户已经存在!"})
            else:
                pass_word = request.POST.get("password", "")
                use_profile = UserProfile()
                use_profile.username = user_name
                use_profile.email = user_name
                use_profile.is_active = False
                use_profile.password = make_password(pass_word)
                use_profile.save()

            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html",{"register_form":register_form})


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,"forgetpwd.html",{"forget_form":forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email,"forget")
            return render(request,"send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetView(View):  # 判断邮箱是否正确，以跳转至修改密码界面
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html",{"email":email})  #传回一个email以判断是哪个用户修改密码
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pw1 = request.POST.get("password1","")
            pw2 = request.POST.get("password2","")
            email = request.POST.get("email","")
            if pw1 != pw2:
                return render(request, "password_reset.html", {"email": email,"msg":"密码前后不一致!"})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pw2) #数据库中修改，密码为密文所有使用make_password函数
                user.save()  #保存

                return render(request,"login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email,"modify_form":modify_form})









# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username","")
#         pass_word = request.POST.get("password","")
#         user = authenticate(username=user_name,password=pass_word)   #认证方法
#         if user is not None:
#             login(request,user)
#             return render(request,"index.html",{})
#         else:
#             return render(request,"login.html",{"msg":"用户名或密码错误!"})
#     elif request.method == "GET":
#         return render(request,"login.html",{})