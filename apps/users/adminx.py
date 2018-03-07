#_*_ encoding:UTF-8 _*_
_author_ = 'IIssNans'
_date_ = '2018/3/6  12:56'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord,Banner


class BaseSetting(object):  #xadmin后台主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "后台管理系统"
    site_footer = "在线学习网"
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):  #管理器
    list_display = ['code','email','send_type','send_time']     #xadmin后台中对数据表的书签显示
    search_fields = ['code','email','send_type']                #xadmin后台中的搜索栏
    list_filter = ['code','email','send_type','send_time']      #xadmin后台中的过滤器


class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)