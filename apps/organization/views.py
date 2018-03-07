#_*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse  #通过这个可以指明返回用户的是什么类型的数据

from .models import CourseOrg,CityDict
from .forms import UserAskForm
from courses.models import Course

# Create your views here.


class OrgView(View):
    '''
    课程机构列表功能
    '''
    def get(self,request):
        #课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:2]  #按点击数取最热门的课程机构，用order_by进行排序，取三个,-为倒序排列即多的在前

        #城市
        all_city = CityDict.objects.all()

        #取出筛选城市
        city_id = request.GET.get('city',"")  #前端点击a标签了后传回city
        if city_id:
            all_orgs = all_orgs.filter(city_id = int(city_id))

        #类别筛选
        category = request.GET.get('ct', "")  # 前端点击了后传回ct
        if category:
            all_orgs = all_orgs.filter(category = category)

        #排序
        sort = request.GET.get('sort',"")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 机构数(进行上面的筛选后进行计数)
        org_num = all_orgs.count()

        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # objects = ['john', 'edward', 'josh', 'frank']  就是all_orgs
        p = Paginator(all_orgs,5, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_orgs":orgs,
            "all_city":all_city,
            "org_num":org_num,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)  #实例化一个userask_form时，把post的数据传进来
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)  #commit为TRUE,直接存取到数据库中
            return HttpResponse('{"status":"success"}',content_type='application/json')         #异步操作ajax，传回的为json格式,json格式为双引号
        else:
            return HttpResponse('{"status":"fail","msg":"添加错误"}',content_type='application/json')  #失败传回form的错误


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        current_page = "home"  #判断选定状态
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]  #取出三个（外键用法）
        all_teachers = course_org.teacher_set.all()[:2]
        return render(request,'org-detail-homepage.html',{
            'current_page':current_page,
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = "course"  # 判断选定状态
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()  # 取出全部（外键用法）
        return render(request, 'org-detail-course.html', {
            'current_page': current_page,
            'all_courses': all_courses,
            'course_org': course_org
        })


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self, request, org_id):
        current_page = "desc"  # 判断选定状态
        course_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            'current_page': current_page,
            'course_org': course_org
        })


class OrgTeacherView(View):
    """
    机构讲师
    """
    def get(self, request, org_id):
        current_page = "teacher"  # 判断选定状态
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()[:2]
        return render(request, 'org-detail-teachers.html', {
            'current_page': current_page,
            'course_org': course_org,
            'all_teachers':all_teachers
        })