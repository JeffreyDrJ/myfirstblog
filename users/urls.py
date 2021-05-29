# 进行users子应用的视图路由
from django.urls import path
from users.views import RegisterView  # 将注册视图导入过来
from users.views import ImageCodeView  # 将图片验证码视图导入过来
from users.views import SmsCodeView   # 短信验证码视图
from users.views import LoginView   # 登录视图
from users.views import LogoutView  # 注销视图
from users.views import ForgetPasswordView  # 忘记密码视图
from users.views import UserCenterView  # 用户中心视图
from users.views import WriteBlogView   # 写文章视图

# 路由、视图函数名制定
urlpatterns = [
    # path的第一个参数： 路由(用于在浏览器中的导航)，从templates文件夹中调取# 第二个参数： 视图函数名

    # 注册页面
    path('register/', RegisterView.as_view(), name='register'),  # 子应用视图函数名设置为users:register
    # 图片验证码
    path('imagecode/',ImageCodeView.as_view(),name='imagecode'),
    # 短信验证码
    path('smscode/',SmsCodeView.as_view(),name='smscode'),
    # 登录页面
    path('login/',LoginView.as_view(),name='login'),
    # 退出登录
    path('logout/',LogoutView.as_view(),name='logout'),
    # 忘记密码
    path('forgetpassword/',ForgetPasswordView.as_view(),name='forgetpassword'),
    # 用户中心
    path('usercenter/',UserCenterView.as_view(),name='usercenter'),
    # 写文章
    # TODO:POTENTIAL writeblog
    path('publish/',WriteBlogView.as_view(),name='publish'),

    ]
