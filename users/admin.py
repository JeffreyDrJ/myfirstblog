from django.contrib import admin

# Register your models here.
# 注册模型以供后台管理：

from .models import User  # (nothing.相当于本文件所处文件夹名.,即users.)

# 注册模型：
admin.site.register(User)
