"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include

# Httpresponse 测试
# logger 设置
# 1. 导入系统的logging
# import logging

# from django.http import HttpResponse


# def log(request):
#     # 2. 创建（获取）日志器
#     logger = logging.getLogger('django_logger')  # getlogger（logger名）
#     # 3. 使用日志器记录信息
#     logger.info('info')
#     return HttpResponse('hope no BUG! QAQ')

# 各子应用的路由引导
# include(arg, namespace=None):urlconf_module(子应用路由), app_name（子应用名字） = arg
urlpatterns = [
    # 1. django自带后台
    path('admin/', admin.site.urls),
    # 2. 日志器跳转
    # path('', log),    # 用于日志器的url引导，进localhost直接跳转到此
    # 3. users子应用跳转
    path('',include(('users.urls','users'),namespace='users')), # 命名空间防止不同子应用名字冲突,也可以被reverse()利用
    # 4. home子应用跳转
    path('',include(('home.urls','home'),namespace='home')),
]
# 追加图片访问引导路由
from django.conf import settings
from django.conf.urls.static import static
# 如果是setting中配置的MEDIA_URL,都引导至MEDIA_ROOT中：
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)