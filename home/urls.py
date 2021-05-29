# home子应用的路由、视图函数名制定
from django.urls import path
from home.views import IndexView    # 主页视图
from home.views import DetailView   # 详细页面视图

urlpatterns = [
    # 1.注册主页
    path('',IndexView.as_view(),name='index'),
    # 2.详细页面
    path('detail/',DetailView.as_view(),name='detail'),

]
