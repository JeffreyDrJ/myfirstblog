from django.db import models    # 自带

# Create your models here.
# 导入django自带库
from django.db import models
from django.contrib.auth.models import AbstractUser  # django自带的用户模型


# 自定义的用户模型：
class User(AbstractUser):   # 继承自AbstractUser
    # 电话号码字段
    # unique 为唯一性字段 blank 为必填
    mobile = models.CharField(max_length=20, unique=True, blank=False)
    # https://blog.csdn.net/u012879957/article/details/105386511/
    # null 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空。
    # blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填，比如 admin 界面下增加 model 一条记录的时候。直观的看到就是该字段不是粗体
    # 通俗点说，该字段null=true后，你进行插入，修改操作时可以为空，然后Django把空值转换成null存在数据库中，而blank只是在表单验证的时候会检测你是否可以为空
    # 头像
    # upload_to为保存到settings：MEDIA（download）的子目录中，不设置的话默认保存到工程根目录,#可在root/settings.py中以MEDIA_ROOT修改；
    avatar = models.ImageField(upload_to='avatars/%Y%m%d/', blank=True)

    # 个人简介
    # max_length 为最大长度
    user_desc = models.TextField(max_length=233, blank=True)

    # 修改认证的字段(父类中原来是username)
    USERNAME_FIELD = 'mobile'

    # 创建超级管理员的需要必须输入的字段(除此之外还需要手机号和密码)
    REQUIRED_FIELDS = ['username', 'email']

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        db_table = 'tb_user'  # 修改默认的表名
        verbose_name = '用户管理'  # Admin后台显示
        verbose_name_plural = verbose_name  # Admin后台显示

    def __str__(self):  # 为了方便调试，重写str方法
        return self.mobile  # 只返回mobile
