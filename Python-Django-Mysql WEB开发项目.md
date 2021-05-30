

# Python-Django-Mysql WEB开发项目

<img src="C:\Users\Jeffrey Ding\Pictures\coding.jpg" alt="coding" style="zoom:80%;" />

### 需求插件：

django3.2、pymysql、redis

### 重要关键词：

root密码**’admin‘!!!**

redis	UUID

#### 库安装代码：

| pip install -i https://pypi.douban.com/simple/ django |
| ----------------------------------------------------- |
| pip install PyMySQL                                   |
|                                                       |
|                                                       |



### 常用指令：

| 代码         | 功能             |
| ------------ | ---------------- |
| ctrl+shift+i | 浏览器开发者工具 |
|              |                  |
|              |                  |



| Python代码                       | 功能                             |
| -------------------------------- | -------------------------------- |
| django-admin startproject [name] | 在当前目录下创建django项目文件夹 |
| python manage.py runserver       | 运行服务器端于8000端口           |
| python manage.py createsuperuser |                                  |
| os.path.join(A+'子路径')         |                                  |

| Mysql代码                                               | 功能                       |
| ------------------------------------------------------- | -------------------------- |
| mysqld --initialize-insecure --user=mysql               | 第一次初始化mysql          |
| mysqld -install                                         | 配置完成mysql              |
| net start mysql                                         | 启动mysql数据库服务        |
| mysql -u root -p                                        | 以user=root访问数据库      |
| mysql> alter user user() identified by "【admin】";     | 在库内修改密码（不漏；）   |
| mysql>quit                                              | 登出数据库                 |
| mysql>show databases;                                   |                            |
| mysql>create database [name];                           | 创建数据库                 |
| mysql>create user [username] identified by '[password]' | 创建新用户与密码           |
| mysql>grant all on [库名].* to '[username]'@'%';        | 赋予user此库所有的表的权限 |
| mysql>flush privileges;                                 | 刷新授权（授权改变后操作） |
| mysql>select *、[id，avatar...] from tb_user;           | 查看表信息                 |
| **Redis代码：**                                         | **功能：**                 |
| redis-server                                            | 开启redis服务              |
| redis-cli                                               | 启动redis客户端            |
| >keys *                                                 | 查看存储内容               |
| redis-server D:\redis\redis.windows.conf                | 报错开启redis              |
| >select 1                                               | 选择1号库                  |
| >FLUSHdb                                                | 删除数据库中信息           |

## 操作步骤：

#### 一、Mysql/Redis数据库初始化，密码重置

#### Mysql:

##### 1.1 解压完mysql后在cmd的操作：

## ![image-20210407195008624](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210407195008624.png)

##### 1.2 修改密码为admin：

![image-20210407195619497](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210407195619497.png)

##### 1.3 创建名为**blog**的数据库（使用utf8字符集）

`create database blog charset utf8;`

![image-20210407201455412](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210407201455412.png)

##### 1.4 添加用户Jeffrey，密码为ding

`create user Jeffrey identified by 'ding';`

![image-20210407202330333](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210407202330333.png)

##### 1.5 赋予Jeffrey对blog库所有表的权限并刷新授权：

`grant all on blog.* to 'Jeffrey'@'%';`

`flush privileges;`

![image-20210407203427394](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210407203427394.png)

##### 1.6 cmd创建django超级用户

`python manage.py createsuperuser`

- 用户名：jeffreyding
- 密码： 16548254z

![image-20210414102937170](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210414102937170.png)

#### Redis:

##### 1.2.1 配置信息：在 blog/settings.py 中

```python
CACHES = {
    "default": { # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": { # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"
```

##### 1.2.2 启动redis服务：

```cmd
D:\redis>redis-server.exe redis.windows.conf
```

![image-20210428104227537](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210428104227537.png)



#### 二、Python操作

##### 2.1 ~~修改解释器路径（意义不明）~~

~~<u>**TNND改了之后p库都没了，目前还是用venv。**</u>~~

![image-20210407204028405](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210407204028405.png)



##### 2.2 修改`settings.py`中的mysql配置信息：

``

```python
DATABASES = {                                   # mysql配置信息
    'default': {
       #  'ENGINE': 'django.db.backends.sqlite3',
         # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',    # 数据库引擎改成mysql
        'HOST': '127.0.0.1',                    # 数据库主机改成localhost
        'PORT': 3306,                           # 数据库端口
        'USER': 'Jeffrey',                      # 数据库用户名
        'PASSWORD': 'ding',                     # 数据库用户密码
        'NAME': 'blog'                          # 数据库名字
    }
}
```

![image-20210407210800195](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210407210800195.png)

2.3 安装`PyMySQL`库并在`_init_.py`中导入

由上步试运行后报错，发现pymysql没装。

`pip install PyMySQL`

![image-20210407211734282](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210407211734282.png)

``

```
import pymysql
pymysql.install_as_MySQLdb()    # 使用了当前虚拟环境的mysql的驱动程序。
```

![image-20210407212344033](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210407212344033.png)

<u>之后出现了`*AttributeError: ‘str‘ object has no attribute ‘decode‘`*报错。</u>

**解决方案：**在`operations.py`里修改utf-8问题代码。![image-20210407214257930](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210407214257930.png)

> *参考资料：https://blog.csdn.net/IT_TIfarmer/article/details/90747496*
>
> *特别鸣谢：ghc*

2.4 日志器的创建（文件输出）

在`settings.py`下加入日志器配置代码：

```python
#  日志
import time

cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        # 日志格式
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
        'simple': {  # 简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    # 过滤
    'filters': {
        # 'require_debug_true': {  # django在debug模式下才输出日志
        #             '()': 'django.utils.log.RequireDebugTrue',
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'all-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'error-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 输出info日志
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'info-{}.log'.format(time.strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',  # 设置默认编码
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'django': { # 定义名为django的日志器
            'handlers': ['default', 'console'], # 同时向终端与文件中输出日志
            'level': 'INFO',    # 日志器接受的最低级别日志
            'propagate': False  # 是否继续传递日志信号
        },
        # log 调用时需要当作参数传入
        'log': {
            'handlers': ['error', 'info', 'console', 'default'],
            'level': 'INFO',
            'propagate': True
        },
    }
}
```

https://www.cnblogs.com/changqing8023/p/9639769.html

*log文件输出位置为BASEDIR下自创的logs文件夹下*（没有也会自创）

*日志器名为： django*

2.4.1 测试`Httpresponse` 和 `logger`：

在`urls.py`下加入：

```python
# Httpresponse 测试
# logger 设置
# 1. 导入系统的logging
import logging

from django.http import HttpResponse


def log(request):
    # 2. 创建（获取）日志器
    logger = logging.getLogger('django_logger')  # getlogger（logger名）
    # 3. 使用日志器记录信息
    logger.info('info')
    return HttpResponse('hope no BUG! QAQ')




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', log),
]
```

结果



#### 

##### 2.5 在 settings 文件的最下方配置添加以下配置：``

```python
STATIC_URL = '/static/' # 别名 
STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, "static"), 
]
```

![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

##### 2.6 在 statics 目录下创建 css 目录，js 目录，images 目录，plugins 目录等， 分别放 css文件，js文件，图片，插件, etc。



### 三、HTML相关操作

#### 1、总体

将静态资源文件分别导入上述文件夹 （用pycharm内置粘贴）

# 四、子应用创建

| 顺序：                         |
| ------------------------------ |
| 创建子应用                     |
| 注册子应用                     |
| 创建模板目录，模板目录设置     |
| 将html导入，定义注册视图       |
| 定义路由，进行工程urls路由引导 |



## 4. 创建users子应用

##### 4.1.1创建

`python manage.py startapp users`

![image-20210412175022426](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210412175022426.png)

##### 4.1.2注册子应用

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',   # 在添加users子应用后，4.12
]
```

##### 4.1.3 标注路径

在bathdir中创建**templates文件夹**（用来放.html文件）

在`settings.py`中templates[]中给出路径：

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],# 给出路径
```

##### 4.1.4 将register.html导入templates文件夹

![image-20210417161350196](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210417161350196.png)

##### 4.1.5 定义注册视图于`views.py`

```python
# 注册视图  @ users/views.py
class RegisterView(View): # registerview继承自view
    def get(self,request):
        return render(request,'register.html')	# 告诉程序到时候渲染的就是这玩意
```

##### 4.1.6 定义路由

在`users`文件夹中新建`urls.py`

```python
# 进行users子应用的视图路由 @users/urls.py
from django.urls import path
from users.views import RegisterView # 将视图导入过来
urlpatterns =[
    # path的第一个参数： 路由(用于在浏览器中的导航)，从templates文件夹中调取
    # 第二个参数： 视图函数名
    path('register/',RegisterView.as_view(),name='register'), # 子应用名
]
```

**注意这里的path是指django.urls的path()!!!**

![image-20210417172041951](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210417172041951.png)

##### 4.1.7 子应用路由引导

**在主程序`urls.py`中的`urlpatterns`下加入：**

```python
# 路由引导   @urls.py
# urlpatterns = [ ...
# include(arg, namespace=None):urlconf_module(子应用路由), app_name（子应用名字） = arg
   path('',include(('users.urls','users'),namespace='users' ))  # 命名空间防止不同子应用名字冲突
```

##### 4.1.8 效果：

![image-20210417195820534](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210417195820534.png)

##### 4.1.9 修改静态文件加载方式

- **一般来说，.css,.gs,.png等加载方式都是通过相对路由方式导入进来的。假如static文件夹位置发生了变化，那么就不能正常导入。**

  通过:

  ```html
  <!-- 修改静态文件加载方式 -->
  {% load staticfiles %}	！！！貌似不行，用static代之
  ```

  例如：

  ```html
  <link rel="stylesheet" href="../static/bootstrap/css/bootstrap.min.css">
  ```

  改为：

  ```html
  <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.min.css' %}">
  ```

以此格式修改所有static下静态资源目录

### 4.2、 用户模型类

##### 4.2.1 Django自带用户模型介绍

django自带的用户模型类：**User(AbstractUser)**

```python
`from django.contrib.auth.models import User, AbstractUser`
```

![image-20210419174520770](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210419174520770.png)

**自定义动机：**

自带的用户模型不含有： **手机号、简介、头像**；因此不能满足需求。因而需要自己定义用户模型类。

##### 4.2.2 创建自定义用户模型类

在`users/models.py`中修改：

```python
from django.db import models    # 自带	@users/models.py

# Create your models here.
# 导入django自带库
from django.db import models
from django.contrib.auth.models import AbstractUser  # django自带的用户模型


# 自定义的用户模型：
class User(AbstractUser):   # 继承自AbstractUser
    # 电话号码字段
    # unique 为唯一性字段 blank 为必填
    mobile = models.CharField(max_length=20, unique=True, blank=False)

    # 头像
    # upload_to为保存到响应的子目录中
    avatar = models.ImageField(upload_to='avatars/%Y%m%d/', blank=True)

    # 个人简介
    # max_length 为最大长度
    user_desc = models.TextField(max_length=233, blank=True)

    # 修改认证的字段
    USERNAME_FIELD = 'mobile'

    # 创建超级管理员的需要必须输入的字段
    REQUIRED_FIELDS = ['username', 'email']

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        db_table = 'tb_user'  # 修改默认的表名
        verbose_name = '用户信息'  # Admin后台显示
        verbose_name_plural = verbose_name  # Admin后台显示

    def __str__(self):  # 为了方便调试，重写str方法
        return self.mobile  # 只返回mobile

```

##### 4.2.3 配置使用的用户模型类

在`settings.py`中添加:

```python
#  替换系统的User 来使用自定义的User(用户模型)
#  配置信息为 ‘子应用名.模型类型’
AUTH_USER_MODEL = 'users.User'
```

##### 4.2.4 迁移文件

```python
terminal>python manage.py makemigrations 
```

```python
ERRORS:
users.User.avatar: (fields.E210) Cannot use ImageField because Pillow is not installed.
        HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "python -m pip install Pillow".
```

装下pillow：

```python
D:\blog>python manage.py makemigrations
Migrations for 'users':
  users\migrations\0001_initial.py
    - Create model User
```

<img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210419220046502.png" alt="image-20210419220046502" style="zoom:67%;" />

app的`migrations`就会产生迁移文件。

##### 4.2.5 链接数据库（迁移前的准备）

<img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210419220538919.png" alt="image-20210419220538919" style="zoom:50%;" />

##### 4.2.6 迁移：注意要先切换到迁移文件：

```python
terminal>python manage.py migrate
```

![image-20210419222653282](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210419222653282.png)

`desc tb_user;` 详细列出`tb_user`表中的参数：  desc- describeの意味

![image-20210419223422866](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210419223422866.png)

##### 4.2.7.Done

### 4.3、图片验证码

##### 4.3.1 准备Captcha包

1. 在`basedir`下创建`libs`库文件夹：**用于存放所需包**。
2. 将captcha文件夹复制到该目录下![image-20210428093924703](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210428093924703.png)

##### 4.3.2 后端接口设计

后端 GET 前端返回的 **UUID**(通用唯一识别码（Universally Unique Identifier）,数据类型string)

#### 4.3.3 后端开发

##### 4.3.3.1在`users/views`里定义图片验证码视图：

安装:

```python
pip install django-redis
```



在users/view.py中：

```python
# 定义图片验证码视图
from django.http.response import HttpResponseBadRequest
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse


class ImageCodeView(View):

    def get(self, request):
        # 1.后端接受前端传递来的 UUID
        uuid = request.GET.get('uuid')
        # 2.判断UUID是否获取成功
        if uuid is None:
            return HttpResponseBadRequest('UUID传递失败！')
        # 3.通过调用Captcha来生成图片验证码（图片二进制，图片内容）
        text,image = captcha.generate_captcha()
        # 4.保存图片内容至redis（以uuid为key，图片内容为value，还要设置一个实效）
        redis_conn = get_redis_connection('default')  # 0号库
        # key设置为 UUID ,添加一个前缀
        # seconds 过期秒数300秒（5分）
        # value 图片二进制内容text
        redis_conn.setex('img:%s'%uuid,300,text)
        # 5.返回图片二进制 （注意因为返回的是图片，要告知返回类型）
        return HttpResponse(image,content_type='image/jpeg')
```

##### 4.3.3.2 在users/urls.py下指定路由与视图函数名：

```python
from users.views import ImageCodeView  # 将图片验证码视图导入过来
```

```python
# 图片验证码
path('imagecode/',ImageCodeView.as_view(),name='imagecode'),
```

##### 4.3.3.3 脑残bug:

解决：在测试中打开redis-cli时不能把redis-server关掉。。

![image-20210429163810395](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210429163810395.png)

[【图文】redis启动报Could not connect to Redis at 127.0.0.1:6379: 由于目标计算机积极拒绝，无法连接。 - 程序员大本营 (pianshen.com)](https://www.pianshen.com/article/89811666555/)

##### 4.3.3.4第一步效果：

![image-20210429163524788](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210429163524788.png)

##### 4.3.3.5修改register.html

原来：

![image-20210429165106140](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210429165106140.png)

其中图片验证码的地址是静态的：

```html
<img src="{% static 'img/image_code.png' %}" @click="generate_image_code" alt="" style="width: 110px;height: 40px;">
```

由`static/js/register.js`中：

![image-20210429165732758](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210429165732758.png)

```html
<img :src="image_code_url" 
```

##### 4.3.3.6 第二部效果：

![image-20210429170030071](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210429170030071.png)

![image-20210429170303428](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210429170303428.png)

可见点击和刷新已经能够生成不同的验证码并返回uuid并保存到redis。

> （以上为blog_429b内容）4.29.17:13

### 4.4、短信验证码

##### 4.4.0 接口设计

###### 4.4.0.1 请求参数：路径参数

| 参数名     | 类型   | 描述                   |
| ---------- | ------ | ---------------------- |
| mobile     | string | 手机号                 |
| image_code | string | 图形验证码（用户输入） |
| uuid       | string | 唯一编号               |

###### 4.4.0.2 响应结果：Json

| 字段   | 说明     |
| ------ | -------- |
| code   | 状态码   |
| errmsg | 错误信息 |



##### 4.4.1 容联云平台 初始化、测试

##### 账号： dingrenjie28@163.com

导入模块至`libs/`



[管理控制台 (yuntongxun.com)](https://www.yuntongxun.com/member/main)

<img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210501212628945.png" alt="image-20210501212628945" style="zoom:50%;" />

<img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210501213206117.png" alt="image-20210501213206117" style="zoom: 50%;" />

在`libs/.../sms`下：

```python
# -*- coding:utf-8 -*-

from libs.yuntongxun.CCPRestSDK import REST

# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8a216da8782428b7017928192d51050a'

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN（账户授权令牌）
_accountToken = '6eaefcc61ec34fa58ddefbdd0e59dec7'

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8a216da8782428b7017928192f310511'

# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'sandboxapp.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = "8883"

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'
```

```python
# 注意： 测试的短信模板编号为1
# 参数1：测试手机号 参数2：列表：您的验证码是{1}，请于{2}分钟内正确输入
# 参数3：短信模板（免费开发测试模板ID为1）
ccp.send_template_sms('13564193353', ['1234', 5], 1)
```

##### 4.4.2 定义短信验证码视图

在`users/views`中：

![image-20210501215922441](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210501215922441.png)

代码：

```python
# 定义短信验证码视图：
from django.http.response import JsonResponse  # 用于网页实时报错->2.1
from utils.response_code import RETCODE  # 用于->2.1
import logging  # 用于->2.2.3,3.1:异常处理记录
from random import randint  # 用于->3.1 生成随机验证码
logger = logging.getLogger('django')
from libs.yuntongxun.sms import CCP # 用于发送验证短信->5


class SmsCodeView(View):

    def get(self, request):

        # 1.接收参数（查询字符串的形式传递过来）
        mobile = request.GET.get('mobile')
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('uuid')

        # 2.参数验证
        # 2.1 参数是否齐全（手机号、图片验证码image_code、uuid）
        if not all([mobile, image_code, uuid]):
            return JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必要参数！'})
        # 2.2 图片验证码验证
        # 2.2.1 链接redis，获取其中的有时效图片验证码：
        redis_conn = get_redis_connection('default')
        redis_image_code = redis_conn.get('img:%s' % uuid)
        # 2.2.2 判断是否存在：
        if redis_image_code is None:
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图片验证码已过期！'})
        # 2.2.3 若未过期，获取后删除图片验证码：(异常处理记录到日志器)
        try:
            redis_conn.delete('img:%s' % uuid)
        except Exception as e:
            logger.error(e)

        # 2.2.3 比对图片验证码（大小写皆可,redis数据类型为bytes,用decode()可以转换）：
        # -如果获取到的redis中bytes通过decode()转换为string在转换为小写形式不等于用户输入的小写string的话：
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入验证码错误！看仔细点-w-'})
        # 3.生成短信验证码并记录
        # 3.1 生成sms_code（6位）
        sms_code = '%06d' % randint(0, 114514)
        # 3.2 记录到日志器
        logger.info(sms_code)
        # 4.保存短信验证码至redis中 (5分钟有效)
        redis_conn.setex('sms:%s' % mobile, 300, sms_code)
        # 5.发送短信    (CCP()为CCP实例化)
        CCP().send_template_sms(mobile,[sms_code,5],1)
        # 6.返回响应
        return JsonResponse({'code':RETCODE.OK,'errmsg':'短信验证码发送成功！'})
```

##### 4.4.3 配置路由URL

在`users/urls`中：

```python
from users.views import SmsCodeView   # 短信验证码视图
```

```python
# 短信验证码
path('smscode/',SmsCodeView.as_view(),name='smscode'),
```

##### 4.4.4代码实现

> POST和GET是HTTP协议定义的与服务器交互的方法。GET一般用于获取/查询资源信息，而POST一般用于更新资源信息
>
> 1.post是取web页面中提交的值
>
> 2.get是从数据库中取值
>
> GET是通过URL传给服务器的,POST是通过HTTP头传给服务器的，post的数据是不跟在请求的url后，而是在http头中，get是在url中
>
> [Django使用POST和GET的区别 - 枫叶少年 - 博客园 (cnblogs.com)](https://www.cnblogs.com/zhansheng/p/11823689.html)

```python
# 定义注册视图
from django.http.response import HttpResponseBadRequest
import re  # 用于正则表达式处理->2.2,2.3
from users.models import User  # 用于保存用户信息->3
from django.db import DatabaseError  # 用于异常处理


class RegisterView(View):  # 继承自View

    def get(self, request):
        return render(request, 'register.html')  # 告诉程序到时候渲染的就是这玩意

    # 实现注册功能：
    def post(self, request):
        # 1.按下注册后，通过post请求收集用户填写的Form表单数据
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        smscode = request.POST.get('sms_code')
        # 2.验证数据
        #     2.1 参数是否齐全
        if not all([mobile, password, password2, smscode]):
            return HttpResponseBadRequest('缺少必要参数！注册失败！lol')
        #     2.2 手机号格式是否正确(从刚开始^的位置开始：以1开始，第二位3-9，后面还有9位,$)
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号格式错误！注册失败！')
        #     2.3 密码格式是否正确
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseBadRequest('请输入至少8位密码！注册失败！')
        #     2.4 二次密码是否一致
        if password != password2:
            return HttpResponseBadRequest('两次密码不一致，注册失败！')
        #     2.5 短信验证码是否和redis中一致
        redis_conn = get_redis_connection('default')
        redis_sms_code = redis_conn.get('sms:%s' % mobile)
        # 2.5.1 短信验证码是否过期
        if redis_sms_code is None:
            return HttpResponseBadRequest('短信验证码已过期！注册失败！')
        if smscode != redis_sms_code.decode():
            return HttpResponseBadRequest('短信验证码错误！注册失败！')
        # 3.保存注册信息
        # 此create()为系统自带方法，密码不能加密；故用create_user(),可用系统自带方法对密码加密
        try:
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
        except DatabaseError as e:
            logger.error(e)
            return HttpResponseBadRequest('注册失败！')
        # 4.返回响应跳转到指定页面
        # TODO: 暂时返回一个注册成功信息，以后实现跳转到指定页面。5.2
        # return HttpResponse('注册成功，重定向到首页。')
        # redirect() 进行重定向
        # reverse() 可以通过namespace:name 来获取视图对应的路由
        return redirect(reverse('home:index'))
```

##### 4.4.5 效果展示

之前：![image-20210502183506668](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210502183506668.png)

之后：

![image-20210502185656254](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210502185656254.png)

> 其中password部分采用了sha256加密

### 4.5、定义登录视图

##### 4.5.1 定义视图

在users/views下：

```python
# 定义登录视图：

class LoginView(View):
    # 因为是在浏览器中获取登录页面：
    def get(self, request):
        return render(request,'login.html')
```

##### 4.5.2 定义路由

在users/urls下：

```python
# 登录页面
path('login/',LoginView.as_view(),name='login'),
```

##### 4.5.3 修改.html文件

- 改static路径以及：

```html
<a href="{% url 'users:register' %} 
```

##### 4.5.4 功能实现：

###### 4.5.4.1 分析：

<img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210502213607922.png" alt="image-20210502213607922" style="zoom:80%;" />

- 注册新账号： 已经通过`login.html`中的a href跳转实现。

- 保持登录：涉及form表单提交

- 接口设计：（请求地址：**/login/**,请求方式:**POST**）

  | 参数名   | 类型   | 概述                   |
  | -------- | ------ | ---------------------- |
  | username | string | 用户名                 |
  | password | string | 密码                   |
  | remember | string | 是否记住用户（非必传） |

  **业务逻辑：**

  ![image-20210502215412101](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210502215412101.png)
  
  ##### 4.5.5 bug 分析
  
  - **1: CSRF问题：**
  
  <img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210503140859144.png" alt="image-20210503140859144" style="zoom: 67%;" />

原因： `login.html`的FORM表单中需要添加:

```html
 <form class="login" id="login_form" method="POST">
                    {% csrf_token %}

```

​            **2:	用户模型问题：**

```python
ERRORS:
users.User: (auth.E002) The field named as the 'USERNAME_FIELD' for a custom user model must not be included in 'REQUIRED_FIELDS'.
	HINT: The 'USERNAME_FIELD' is currently set to 'username', you should remove 'username' from the 'REQUIRED_FIELDS'.

System check identified 1 issue (0 silenced).
```

原因： 由于AbstractUser模型默认问题，在继承类中修改之： `users/models`:

```python
# 修改认证的字段(父类中原来是username)
USERNAME_FIELD = 'mobile'
```

##### 4.5.6 效果

<img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210503145011600.png" alt="image-20210503145011600" style="zoom: 67%;" />

### 4.6、登录状态展示

##### 4.6.0 cookie信息通过.js获取： index.js

```javascript
var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        show_menu:false,
        is_login:true,
        username:''
    },
    mounted(){
        this.username=getCookie('username');
        this.is_login=getCookie('is_login');
        // this.is_login=true	# 原来的代码
    },
    methods: {
        //显示下拉菜单
        show_menu_click:function(){
            this.show_menu = !this.show_menu ;
        },
    }
});
```

##### 4.6.1按照.js文件获取cookie信息链接到.html中：

```html
<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" @click="show_menu_click">admin</a>
```

- 将admin 修改为: [[username]]

##### 4.6.2 效果：

![image-20210503152343774](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210503152343774.png)

### 4.7、退出登录

##### 4.7.1 分析：

- 登录是将通过认证的用户的唯一标识信息写入当前session会话中。

- 反之，退出登录就是要清理session会话信息。

- ```python
  logout(request)
  ```

  

  - Django自带的方法，封装了清理session的操作
  - `django.contrib.auth._init_.py`

##### 4.7.2 定义注销视图

于users/views:

```python
# 定义注销视图：
from django.contrib.auth import logout


class LogoutView(View):

    def get(self, request):
        # 1.session数据清除
        logout(request)
        # 2.cookie数据部分删除
        response = redirect(reverse('home:index'))
        response.delete_cookie('is_login')
        # 3.跳转到首页
        return response
```

##### 4.7.3 定义路由

于users/urls:

```python
# 退出登录
path('logout/',LogoutView.as_view(),name='logout'),
```

##### 4.7.4 与.html链接

于index.html:

```html
<a class="dropdown-item" href='#'>退出登录</a>
```

```html
<a class="dropdown-item" href='{% url 'users:logout' %}'>退出登录<
```

##### 4.7.5 bug

退出登录后无法通过v-else变成登录

### 4.8 忘记密码

##### 4.8.1 定义忘记密码视图

```python
# 定义忘记密码视图：

class ForgetPasswordView(View):

    def get(self, request):
        return render(request, 'forget_password.html')
```

##### 4.8.2 定义路由

```python
# 忘记密码
path('forgetpassword/',ForgetPasswordView.as_view(),name='forgetpassword'),
```

##### 4.8.3 通过.js里的参数将图片验证码修改成动态地址

在forget_password.html下:

```html
<!--改成由forget_password.js,line46下定义的动态链接-->
<img :src="image_code_url" @click="generate_image_code" alt="" style="width: 110px;height: 40px;">
```

##### 4.8.4 功能实现

###### 4.8.4.1 分析：

<img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210503184906462.png" alt="image-20210503184906462" style="zoom:80%;" />

###### 4.8.4.2 实现：

```python
# 定义忘记密码视图：

class ForgetPasswordView(View):

    def get(self, request):
        return render(request, 'forget_password.html')

    def post(self, request):
        # 1.接受数据表单
        mobile = request.POST.get('mobile')
        new_password = request.POST.get('password')
        new_password2 = request.POST.get('password2')
        smscode = request.POST.get('sms_code')
        # 2.验证数据
        # 2.1参数是否齐全（手机号，新密码，二次新密码，短信验证码）
        if not all([mobile, new_password, new_password2, smscode]):
            return HttpResponseBadRequest('输入参数不全！')
            # 2.2手机号格式
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号格式错误!')
            # 2.3新密码格式
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', new_password):
            return HttpResponseBadRequest('新密码格式不符合：8-20位非符号!')
            # 2.4确认新密码是否一致
        if new_password2 != new_password:
            return HttpResponseBadRequest('两次密码输入不一致！')
            # 2.5短信验证码检测（redis中）
        redis_conn = get_redis_connection('default')
        redis_sms_code = redis_conn.get('sms:%s' % mobile)
        if redis_sms_code is None:
            return HttpResponseBadRequest('短信验证码已过期！请重试')
        if redis_sms_code.decode() != smscode:
            return HttpResponseBadRequest('短信验证码输入错误，重试看看！')
        # 3.根据手机号进行用户查询
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 4.反馈
            # 4.1如果没查到，就进行新用户创建
            try:
                User.objects.create_user(username=mobile, mobile=mobile, password=new_password)
            except Exception as e:
                logger.error(e)
                return HttpResponseBadRequest('自动注册新用户失败。。GGWP')
        else:
            # 4.2如果查到了，修改之
            user.set_password(new_password)
            # 注意要保存用户信息!!!
            user.save()
        # 5.页面跳转至 登陆页面
        response = redirect(reverse('users:login'))
        # 6.返回响应
        return response
```

### 4.9、用户中心

##### 4.9.1 定义视图

省略

##### 4.9.2 定义路由

省略

##### 4.9.3 用户中心禁止非登录用户查看

###### 4.9.3.1 分析：

- 自带登录验证：`request.user.is_authenticated()`: True/False

- from django.contrib.auth.mixins import LoginRequiredMixin

  - 如果用户未登录，则进行默认跳转，默认跳转链接为：accounts/login/?next=/usercenter/,accounts/login/+查询字符串

  - **前面的默认跳转链接可在root/settings.py中修改；next=/.../用于回跳**

###### 4.9.3.2功能实现：

1.导入功能：

```python
from django.contrib.auth.mixins import LoginRequiredMixin  # 混入扩展功能，实际上还是调用了`request.user.is_authenticated()`
```

2.修改未登录默认跳转：

在**settings.py**下：

```python
# 修改系统的未登录默认跳转链接：
LOGIN_URL='/login/'
```

3. 回跳实现：

   在 loginView中

   ```python
   # response = redirect(reverse('home:index'))
   # extra: 根据mixin中next参数进行判断页面跳转：
   next_page = request.GET.get('next') # 判断url中有没有这个关键字参数
   if next_page: # 如果有：
       response = redirect(next_page)
   else:
       response = redirect(reverse('home:index'))
   ```

4.9.4 前端从后端获得用户信息并显示：

在users/views：

```python
class UserCenterView(LoginRequiredMixin, View):
    def get(self, request):
        # 前端获得登录用户的信息：
        user = request.user
        # 前端组织获取用户信息：
        context ={
            'username':user.username,
            'mobile':user.mobile,
            # 如果头像存在的话获取头像，否则返回None
            'avatar':user.avatar.url if user.avatar else None,
            'user_desc':user.user_desc
        }
        return render(request, 'center.html',context=context)
```

在center.html中：

```html
<br> <div class="col-md-4">头像</div>
    <!--进行判断：从返回前端的context中： -->
    {% if avatar %}
        <img src="{{avatar}}" style="max-width: 20%;" class="col-md-4"><br>
        <!--没有的话还是显示默认头像 -->
    {% else %}
        <img src="{% static 'img/mei.png' %}" style="max-width: 20%;" class="col-md-4"><br>
    {% endif %}
```

```html
<!-- 文本区域 -->
<textarea type="text" class="form-control" id="desc" name="desc" rows="12" >{{ user_desc }}</textarea>
```

##### 4.9.4  修改个人中心数据

###### 4.9.4.1 分析：POST表单

| 参数名   | 类型   | 作用     |
| -------- | ------ | -------- |
| username | string | 用户名   |
| avatar   | file   | 头像     |
| desc     | string | 个人简介 |

![image-20210503212553488](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210503212553488.png)

###### 4.9.4.2 功能实现：

```python
def post(self,request):
    # 业务逻辑：
    # 1.接收参数
    konouser = request.user
    update_username = request.POST.get('username',konouser.username) # (如果没有传递的话还是用之前的用户信息)
    update_user_desc = request.POST.get('desc',konouser.user_desc)
    # 头像信息为ImageField（models.py），为file类型
    update_avatar = request.FILES.get('avatar') # 保底判断在center.html里
    # 2.将参数保存入库
    try:
        konouser.username = update_username
        konouser.user_desc = update_user_desc
        if update_avatar:
            konouser.avatar = update_avatar
        konouser.save() # 注意保存
    except Exception as e:
        logger.error(e)
        return HttpResponseBadRequest('修改失败！重新试试？')
    # 3.刷新当前页面（重定向）
    response = redirect(reverse('users:usercenter'))
    # 4.更新cookie中的username信息
    response.set_cookie('username',konouser.username,max_age=14*24*3600)
    # 5.返回响应
    return response
```

###### 头像保存路径：从models可见：

```python
# 头像
# upload_to为保存到响应的子目录中，不设置的话默认保存到工程根目录,#可在root/settings.py中以MEDIA_ROOT修改；
avatar = models.ImageField(upload_to='avatars/%Y%m%d/', blank=True)
```

**注意这里是在basedir/download/avatars/...的意思**

###### 来到settings.py下添加：

```python
# 设置上传的头像至blog/download/
MEDIA_ROOT = os.path.join(BASE_DIR,'download/')
```

###### 4.9.4.3 问题：

![image-20210503221604050](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210503221604050.png)![image-20210503221615871](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210503221615871.png)![image-20210503221632686](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210503221632686.png)

可见数据库和文件目录内都有了，但是不显示。

**原因：**[Page not found at /avatars/20210503/cat_eng_square.png

[](http://127.0.0.1:8000/avatars/20210503/cat_eng_square.png)

路径少了那么一段/download/

**需要设置图片访问的统一路由：**

```python
# 设置图片访问的统一路由（用来解决头像不显示，路径错误http://127.0.0.1:8000/avatars/20210503/）
MEDIA_URL = '/download/'
# 这时候会变成/download/avatar/...
```

最后在blog/urls.py下：

```python
# 追加图片访问引导路由
from django.conf import settings
from django.conf.urls.static import static
# 如果是setting中配置的MEDIA_URL,都引导至MEDIA_ROOT中：
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
```

done.

###### 4.9.4.4效果展示：

<img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210503224046810.png" alt="image-20210503224046810" style="zoom:67%;" />

### 4.10、写博客

#### 4.10.1 定义视图

users/views:

```python
# 定义写文章视图：


class WriteBlogView(View):
    def get(self,request):

        return render(request,'write_blog.html')
```

#### 4.10.2 定义路由

users/urls:

```python
# 写文章
# TODO:POTENTIAL writeblog
path('publish/',WriteBlogView.as_view(),name='publish'),
```

#### 4.10.3 文章分类

##### 4.10.3.1 创建文类模型

在home/models下：

```python
# 自定义文类模型：
class ArticleCategory(models.Model):
    # 1.分类标题
    title = models.CharField(max_length=100, blank=True, help_text='blank=True是允许表单验证为空')
    # 2.分类创建时间
    createdtime = models.DateTimeField(default=timezone.now)

    # 3.为了admin站点显示、调试方便：添加str方法等：
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_category'  # 修改表名
        verbose_name = '类别管理'   # admin站点显示
        verbose_name_plural = verbose_name  # 复数形式和单数一样
```

##### 4.10.3.1 注册子应用

blog/settings:

```python
'home.apps.HomeConfig', # 子应用home 注册
```

##### 4.10.3.2 生成迁移文件并迁移

```python
>python manage.py makemigrations
```

```python
>python manage.py migrate	#注意要先切换到迁移文件：
```

效果：<img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210503234529207.png" alt="image-20210503234529207" style="zoom:67%;" />![image-20210503234707184](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210503234707184.png)

##### 4.10.3.3 通过admin站点后台管理文类

1. 注册超级管理员：

   <img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504133345656.png" alt="image-20210504133345656" style="zoom:80%;" />

**密码： password**

2. 注册模型：

   到`home/admin.py`下，注册home/model下的**ArticleCategory**:

   ```python
   from home.models import ArticleCategory
   # 注册模型：
   admin.site.register(ArticleCategory)
   ```

   <img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504134131301.png" alt="image-20210504134131301" style="zoom:67%;" />![image-20210504135320174](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504135320174.png)

   > ”类别管理“  来源于home/models.py中的class Meta中的定义：

   ```python
   class Meta:
       db_table = 'tb_category'  # 修改表名
       verbose_name = '类别管理'   # admin站点显示
   ```

![image-20210504135748248](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504135748248.png)

**但此时写博客页面下还是看不到新板块。**

##### 4.10.3.4 写博客页面展示分类

1. 修改.html下的栏目功能：

   原：![image-20210504140631279](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504140631279.png)

   改：**通过for语句进行循环，显示前端索取的context：**

   ```python
   # 定义写文章视图：（回跳功能已经在RegisterView下实现）
   from home.models import ArticleCategory  # 用于写博客页面展示文类
   
   
   # 同样需要先登录才能写：
   class WriteBlogView(LoginRequiredMixin, View):
       def get(self, request):
           # 查询所有分类模型
           categories = ArticleCategory.objects.all()
   
           context = {
               'categories':categories
           }
           return render(request, 'write_blog.html',context=context)
   ```

   ```html
   <!-- 文章栏目 write_blog.html-->
   <div class="form-group">
       <label for="category">栏目</label>
       <select class="form-control col-3" id="category" name="category">
               <option value="none">--请选择栏目:D--</option>
               {% for category in categories%}
                   <option value="{{ category.id }}">{{ category.title }}</option>
               {% endfor %}
       </select>
   </div>
   ```

2. 效果：

   <img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504141518592.png" alt="image-20210504141518592" style="zoom:67%;" />

#### 4.10 定义文章模型类

封面图，标签tag，标题，摘要，浏览量，评论量，发布时间，作者，修改时间，正文

```python
# 文章模型：	# home/models.py
from users.models import User  # 用于保存作者的外键
from django.utils import timezone # 用于保存创建时间，修改时间


class Article(models.Model):
    # 保存内容：作者，标题图，标题，分类，标签，摘要，正文，创建时间，浏览数，评论数，修改时间
    # ----------------------------------------------------------------------
    # 1.作者
    # (外键是用来连接两个表的键。一个外键是一个指向另一个表中的primary key的字段(或字段的集合),这里指向user信息
    # on_delete: 当user表中的数据更新、删除后，文章信息中也同步更新、删除（一致性确保）
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    # 2.标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/',blank=True)
    # 3.标题
    title = models.CharField(max_length=20,blank=True)
    # 4.分类
    # related_name:和之前的_set操作的效果是一样的，这两个方法是相同的，所以如果觉得比较麻烦的话，可以在定义主表的外键的时候，直接就给外键定义好名称使用related_name
    # https://blog.csdn.net/hpu_yly_bj/article/details/78939748

    category = models.ForeignKey(ArticleCategory,null=True,blank=True,related_name='articles',on_delete=models.CASCADE)
    # 5.标签
    tags = models.CharField(max_length=20,blank=True)
    # 6.摘要
    summary = models.CharField(max_length=200,null=True)
    # 7.正文
    content = models.TextField()
    # 8.浏览量
    total_views = models.PositiveIntegerField(default=0)
    # 9.评论量
    total_comments = models.PositiveIntegerField(default=0)
    # 10.文章创建时间
    created_time = models.DateTimeField(default=timezone.now)
    # 11.文章修改时间
    # auto_now:无论你是添加还是修改对象，时间为你添加或者修改的时间，相当于更新时间。
    # https://blog.csdn.net/Ayue1220/article/details/92210205
    updated_time = models.DateTimeField(auto_now=True)
    # 方便调试：
    def __str__(self):
        return self.title
    # 数据库、后端管理相关：
    
    class Meta:
        db_table = 'tb_article'  # 修改表名
        # 默认排序(优先按照发布时间排序)
        # https://baijiahao.baidu.com/s?id=1644529735187445459&wfr=spider&for=pc
        ordering = ('-created_time','title')
        verbose_name = '文章管理'  # admin站点显示
        verbose_name_plural = verbose_name  # 复数形式和单数一样
```

![image-20210504152143131](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504152143131.png)

#### 4.11 博客发布（功能实现）

```python
# 实现博客保存功能 2021.5.4
def post(self, request):
    # 1.接收数据
    avatar = request.FILES.get('avatar')
    title = request.POST.get('title')
    category_id = request.POST.get('category')
    tags = request.POST.get('tags')
    summary = request.POST.get('summary')
    content = request.POST.get('content')
    author = request.user
    # 2.认证数据
    # 2.1参数是否齐全
    if not all([avatar, title, category_id, summary, content]):
        return HttpResponseBadRequest('参数没写全，不收录！-へ-')
        # 2.2分类id判断
    try:
        confirm_category_obj = ArticleCategory.objects.get(id=category_id)
    except ArticleCategory.DoesNotExist:
        return HttpResponseBadRequest('没有此分类哦~')
    # 3.保存入库
    try:
        article = Article.objects.create(
            title=title,
            author=author,
            avatar=avatar,
            category=confirm_category_obj,
            tags=tags,
            summary=summary,
            content=content
        )
    except Exception as e:
        logger.error(e)
        return HttpResponseBadRequest('数据库相关错误，无法发布orz')# 注意标题不能带字符！！！！
    # 4.跳转
    response = redirect(reverse('home:index'))
    # 5.返回响应
    return response
```

![image-20210504160947725](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504160947725.png)





## 5、首页展示（创建home子应用）

#### 5.1 初始化

1. python manage.py startapp home

2. 创建urls.py

3. 导入index.html

4. 在`home/views`下链接html来渲染视图：

   ```python
   class IndexView(View):
       def get(self, request):
   
           return render(request, 'index.html')
   ```

5. 在`blog/urls`下添加home子应用的路由引导：

   ```python
   # 4. home子应用跳转
   path('',include(('home.urls','home'),namespace='home')),
   ```

6. 修改一些跳转参数：

   如：

   ```html
   <!-- 导航栏商标 -->
   <div>
       <a class="navbar-brand" href="./index.html">个人博客</a>
   ```

   改为：

   ```http
   <!--    <a class="navbar-brand" href="./index.html">个人博客</a> -->
       <a class="navbar-brand" href="{% url 'home:index' %}">个人博客</a>
   ```

#### 5.2、首页板块（文类）展示：

##### 5.2.1功能分析：

- 首页get到mysql中的category信息，渲染出来；高亮显示
- 内容筛选到只有相同category的ariticle

##### 5.2.2 views视图实现：

```python
# 定义首页视图
from django.views import View

# ------------------------
from home.models import ArticleCategory
from django.http.response import HttpResponseNotFound


class IndexView(View):
    def get(self, request):
        # 1.后端获取数据库中分类信息
        categories = ArticleCategory.objects.all()
        # 接受用户点击的分类id#TODO:cat_id?
        cat_id = request.GET.get('cat_id', 1)  # 若未传递，默认值1
        # 2.根据分类id进行分类查询
        try:
            selected_category = ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('未在数据库中找到此文类ArticleCategory not found！！')
        # 3.组织数据传递给模板.html
        context = {
            'categories': categories,
            'selected_category': selected_category
        }
        return render(request, 'index.html', context=context)
```

##### 5.2.3 模板.html中实现（模板填充）：

- 分类被点击后，class里会有active

原来：

<img src="C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504163645091.png" alt="image-20210504163645091" style="zoom:80%;" />

改为：

```html
<!-- 分类 -->
<div class="collapse navbar-collapse">
    <div>
        <ul class="nav navbar-nav">
        <!--遍历找到选中的文类，href='/?var=x'查询字符串功能   传入categories->试cat_id-html通过浏览器的get请求通过url返回给浏览器--后台判断出selected--传给前端判断给出active-->
            {% for cat in categories %}
                {% if cat.id == selected_category.id %}
                    <li class="nav-item active">
                        <a class="nav-link mr-2" href="/?cat_id={{ cat.id }}">{{ cat.title }}</a>
                    </li>
                {% else %}
                    <li class="nav-item">
                         <a class="nav-link mr-2" href="/?cat_id={{ cat.id }}">{{ cat.title }}</a>
                    </li>
                {% endif %}
            {% endfor %}
        </ul>
    </div>
```

效果：![image-20210504170659241](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504170659241.png)

#### 5.3、首页文章展示，分页

```python
from home.models import ArticleCategory
from home.models import Article
from django.http.response import HttpResponseNotFound
from django.core.paginator import Paginator,EmptyPage


class IndexView(View):
    def get(self, request):
        # 1.后端获取数据库中分类信息
        categories = ArticleCategory.objects.all()
        # 2.浏览器从html接受用户点击的分类id
        cat_id = request.GET.get('cat_id', 1)  # 若html未传递，默认值1
        # 3.根据用户点击的分类id进行分类查询
        try:
            selected_category = ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('未在数据库中找到此文类ArticleCategory not found！！')
        # 4.从html获取分页参数
        page_num = request.GET.get('page_num',1)    # 目前页数，非总页数
        page_size = request.GET.get('page_size',10) # 单页对象数
        # 5.获取分类信息筛选文章数据
        filtered_articles = Article.objects.filter(category=selected_category)  # 注意这里是对象
        # 6.创建分页器
        # (self, object_list, per_page, orphans=0,allow_empty_first_page=True)

        paginator = Paginator(filtered_articles,per_page=page_size)
        # 7.进行分页处理
        try:
            page_articles = paginator.page(page_num)
        except EmptyPage:
            return HttpResponseNotFound('empty page!')
        # 8.获取总页数
        total_page_num = paginator.num_pages
        # 8.组织数据传递给模板.html
        context = {
            # 分类参数
            'categories': categories,
            'selected_category': selected_category,
            # 分页参数
            'articles':page_articles,
            'page_size':page_size,
            'page_num':page_num,
            'total_page':total_page_num
        }
        return render(request, 'index.html', context=context)
```

##### 分页：

```html
 $(function () {
        $('#pagination').pagination({
            currentPage: {{page_num}},
            totalPage: {{total_page}},
            callback:function (current) {
<!--TODO:通过查询字符串分页跳转-->
                {# ?cat_id=3&page_size=10&page_num=2 #}
                location.href = '/?cat_id={{selected_category.id}}&page_size={{ page_size }}&page_num='+current;
            }
        })
    });
</script>
</body>
</html>
```

效果：![image-20210504215901746](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504215901746.png)

#### 5.4、文章详细页面

##### 5.4.1 思路：

文章详细页面可以通过查询字符串的id返回过来

![image-20210504222440792](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504222440792.png)

![image-20210504222651882](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504222651882.png)

##### 5.4.2 实现：

```python
class DetailView(View):
    def get(self, request):
        # 业务逻辑：
        # 1.接收文章id信息
        id = request.GET.get('article_id')
        # 2.根据文章id进行文章数据查询
        try:
            selected_article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            pass	## （404页面部分）#####################
        # 3.查询分类数据(用于上边条板块高亮、跳转)
        categories = ArticleCategory.objects.all()
        # 4.组织模板数据
        context = {
            'categories':categories,
            'category':selected_article.category,
            'article':selected_article
        }
        return render(request, 'detail.html',context=context)
```

##### 修改index.html：

- 点击标题时跳转，同时给出一个查询字符串**?article_id={{article.id}}**

  使得home/views中get到并且判断跳转后的**显示内容**。

**修改detail.html:**

- 改上边栏板块高亮

- 填充详细页面内显示内容

#### 5.5、404页面

```python
# 2.根据文章id进行文章数据查询
try:
    selected_article = Article.objects.get(id=id)
except Article.DoesNotExist:
    return render(request,'404.html')   # 若没有这个articleid总不能啥也不显示，所以跳转到404页面
```

#### 5.6、更新浏览量，根据其进行推送

- **在home/views:**

```python
# 2.根据文章id进行文章数据查询
try:
    selected_article = Article.objects.get(id=id)
except Article.DoesNotExist:
    return render(request,'404.html')   # 若没有这个articleid总不能啥也不显示，所以跳转到404页面
else:
    # 浏览量+1
    selected_article.total_views += 1
    selected_article.save()
# 3.查询分类数据(用于上边条板块高亮、跳转)
categories = ArticleCategory.objects.all()
# 4.查询浏览量前10的文章
# 用.order_by排序，-为降序
popular_articles = Article.objects.order_by('-total_views')[0:9]
```

- **在detail.html:**

```html
<!-- 推荐循环，通过popular_articles -->
<div class="col-3 mt-4" id="sidebar" class="sidebar">
    <div class="sidebar__inner">
            <h4><strong>站长推荐</strong></h4>
            <hr>
            {% for article in popular_articles %}
                <a href="{% url 'home:detail' %}?article_id={{ article.id }}" style="color: black">{{ article.title}}</a><br>
            {% endfor %}
```

- 效果：

  ![image-20210505110141532](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210505110141532.png)

#### 5.7 定义评论模型

##### 5.7.1 内容：

- **针对文章，用户名，时间，内容**

##### 5.7.2 定义模型类：

```python
# 自定义评论模型：


class Comment(models.Model):
    # 保存内容：针对文章，用户名，时间，内容
    # -----------------------------------
    # 1.评论内容
    content = models.TextField(max_length=100)
    # 2.评论文章
    target_article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    # 3.评论用户
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    # 4.评论时间
    created_time = models.DateTimeField(auto_now=True)

    # str方法：
    def __str__(self):
        return self.target_article.title

    # 数据库相关：
    class Meta:
        db_table = 'tb_comment'
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name
```

#### 5.8 发表评论

##### 5.8.1 根据点击发送，post发表内容content，get获取（用户信息，文章id），若session没登陆，那么不能上传数据库，先跳转到登陆

![image-20210505141616489](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210505141616489.png)

```python
def post(self, request):
    # 业务逻辑：
    # 1.接收用户信息
    user = request.user
    # 2.判断用户是否存在+登录
    if user and user.is_authenticated:
        # 4 登录用户接收表单post：
        target_id = request.POST.get('hidden_id')     # 注意这里是接受来自html的隐藏域，だが、どうして？
        content = request.POST.get('content')
        # 5. 验证文章id存在性
        try:
            target_article = Article.objects.get(id=target_id)
        except Article.DoesNotExist:
            return HttpResponseNotFound('没有此文章。')

        # 6. 评论入库
        Comment.objects.create(
            content=content,
            target_article=target_article,
            user=user
        )
        # 7. 修改评论数量
        target_article.total_comments += 1
        target_article.save()
        # 8. 跳转(当前页面:detail目录+文章id)
        path = reverse('home:detail') + '?article_id={}'.format(target_id)
        return redirect(path)

    else:
        # 3 未登录跳转
        return redirect(reverse('users:login'))
```

```html
<form method="POST">
    {% csrf_token %}
    <!--此时表单中只有content内容，但没有id信息    -->
    <!-- 隐藏域在页面中对于用户是不可见的，在表单中插入隐藏域的目的在于收集或发送信息，以利于被处理表单的程序所使用。浏览者单击发送按钮发送表单的时候，隐藏域的信息也被一起发送到服务器。 -->
   <input type="hidden" name="hidden_id" value="{{ article.id }}">
<div class="form-group"><label for="body"><strong>我也要发言：</strong></label>
    <div>
```

#### 5.9 评论、页码显示

```python
class DetailView(View):
    def get(self, request):

        # 文章详情显示&评论显示&页码显示的业务逻辑：
        # 1.从index跳转到detail时附加的?id={{article.id}}接收文章id信息
        show_article_id = request.GET.get('article_id')
        # 2.根据文章id进行文章数据查询
        try:
            selected_article = Article.objects.get(id=show_article_id)
        except Article.DoesNotExist:
            return render(request, '404.html')  # 若没有这个articleid总不能啥也不显示，所以跳转到404页面
        else:
            # 浏览量+1
            selected_article.total_views += 1
            selected_article.save()
        # 3.查询分类数据(用于上边条板块高亮、跳转)
        categories = ArticleCategory.objects.all()
        # 4.查询浏览量前10的文章
        # 用.order_by排序，-为降序
        popular_articles = Article.objects.order_by('-total_views')[0:9]
        # a.获取分页信息
        page_size = request.GET.get('page_size',10)
        page_num = request.GET.get('page_num',1)
        # b.根据文章信息查询评论数据
        comments = Comment.objects.filter(target_article=selected_article).order_by('-created_time')
        # c.获取评论总数  (# todo:为什么不用selected_article.total_comments?)
        comment_count = comments.count()
        # d.创建分页器
        from django.core.paginator import Paginator,EmptyPage
        paginator = Paginator(comments,page_size)
        # e.分页处理
        try:
            page_comments = paginator.page(page_num)
        except EmptyPage:
            return HttpResponseNotFound('评论分页出错.empty page-orz')
        # f.总页数获取
        total_page = paginator.num_pages
        # 4.组织模板数据
        context = {
            'categories': categories,               # 所有板块
            'category': selected_article.category,  # 浏览的板块
            'article': selected_article,            # 浏览的文章
            'popular_articles': popular_articles,   # 推荐的10篇文章
            'comment_count':comment_count,          # 评论总数
            'comments':page_comments,               # 本页评论
            'page_size':page_size,                  # 页大小
            'total_page':total_page,                # 总页数
            'page_num':page_num                     # 当前页数
        }
        return render(request, 'detail.html', context=context)
```





## 6、状态保持

##### 6.1 注意事项

- 用户信息是在cookie中获取并展示，因此需要设置cookie信息，需要到response中设置

- cookie：**基于键值对的形式存储**；设置cookie：通过HttpResponse响应对象中的set_cookie来设置：HttpResponse.set_cookie('name',value = 'wjm',max_age = 3600)

  max_age默认单位为秒，若不设置则为None

  - cookie是通过.js来获取的

##### 6.2 操作

在users/views下，注册实现跳转前：

```python
# 4.注册后状态保持（免登录）
        from django.contrib.auth import login
        login(request,user)
        # 5.返回响应跳转到指定页面
        # TODO: 暂时返回一个注册成功信息，以后实现跳转到指定页面。2021.5.2
        # return HttpResponse('注册成功，重定向到首页。')
        # redirect() 可以进行重定向
        # reverse() 可以通过namespace:name 来获取视图对应的路由
        # return redirect(reverse('home:index'))
        # cookie需要到response中设置
        response = redirect(reverse('home:index'))
        # 设置2个cookie信息（判断，展示），以方便首页中用户信息展示的判断和用户信息的展示
        response.set_cookie('is_login',True) # 展示
        response.set_cookie('username',user.username,max_age=7*24*3600)
        return response
```

##### 6.3 效果

![image-20210502203654435](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210502203654435.png)

### 7、DIY优化功能

##### 7.1 TODO:缺图测试

修改了文章类Article中必须传递标题图avatar的特性：

```python
# 2.标题图 #TODO:缺图测试#home/models.py
avatar = models.ImageField(upload_to='article/%Y%m%d/',blank=True,null=True)
```

在index.html中插入判断，加入缺省图，防止渲染错误：

```html
<!-- 文章内容 -->
<!-- 标题图 TODO:缺图测试-->
<div class="col-3">
    {% if article.avatar %}
        <img src="{{ article.avatar.url }}" alt="avatar" style="max-width:100%; border-radius: 20px">
    {% else %}
        <img src="{% static 'img/no_avatar.png' %}" alt="avatar" style="max-width:100%; border-radius: 20px">
    {% endif %}
</div>
```

效果：

![image-20210504211943783](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210504211943783.png)

##### 7.2 404图片DIY

原来：<img src="../static/img/404g.gif" alt="">

```html
<div style="text-align: center;">
    <a href="/" class="primaryAction btn btn-primary">返回首页</a>
</div>
```

**改成：**

贴图部分：在<head内：

```html
<style>
    body {
        background-image: url("{% static 'img/404g.gif' %}");
        background-position: center;
    }
</style>
```

按钮部分：

```html
<div style="margin-left:500px;margin-top:500px;">
    <a href="/" class="primaryAction btn-lg btn-primary">返回首页</a>
</div>
```

效果：

![image-20210505000655606](C:\Users\Jeffrey Ding\AppData\Roaming\Typora\typora-user-images\image-20210505000655606.png)

```
<footer class="py-3 modal-footer" id="footer" style="background:#f0c674"> -->
    <div class="container">
        <h5 class="m-0 text-center text-light">JeffreyD的bug博物馆</h5>
    </div>
</footer>
</div>
```

```html
<!-- content -->
<div class="container">
    <!-- 列表循环-显示板块文章概述内容 TODO:添加‘所有‘板块 -->
    {% for article in articles %}
        <div class="row mt-2">
            <!-- 文章内容 -->
            <!-- 标题图 TODO:缺图测试-->
            <div class="col-3">
                {% if article.avatar %}
                    <img src="{{ article.avatar.url }}" alt="avatar" style="max-width:100%; border-radius: 20px">
                {% else %}
                    <img src="{% static 'img/no_avatar.png' %}" alt="avatar" style="max-width:100%; border-radius: 20px">
                {% endif %}
            </div>
            <div class="col">
                <!-- 栏目 -->
                <a  role="button" href="#" class="btn btn-sm mb-2 btn-warning">{{ article.category.title }}</a>
            <!-- 标签 -->
                <span>
                        <a href="#" class="badge badge-secondary">{{ article.tags }}</a>
                </span>
                <!-- 标题 -->
                <h4>
                    <!--跳转时article.id给到views从而使得details.html里的article得到锁定 -->
                    <b><a href="{% url 'home:detail' %}?article_id={{ article.id }}" style="color: black;">{{ article.title }}</a></b>
                </h4>
                <!-- 摘要 -->
                <div>
                    <p style="color: gray;">
                        {{ article.summary }}
                    </p>
                </div>
                <!-- 注脚 -->
                <p>
                    <!-- 查看、评论、时间 -->
                    <span><i class="fas fa-eye" style="color: lightskyblue;"></i>{{ article.total_views }}&nbsp;&nbsp;&nbsp;</span>
                    <span><i class="fas fa-comments" style="color: yellowgreen;"></i>{{ article.total_comments }}&nbsp;&nbsp;&nbsp;</span>
                    <span><i class="fas fa-clock" style="color: pink;"></i>{{ article.created_time|date }}</span>
                </p>
            </div>
            <hr style="width: 100%;"/>
    </div>
    {% endfor %}







    <!-- 页码导航 -->
    <div class="pagenation" style="text-align: center">
        <div id="pagination" class="page"></div>
    </div>
</div>

<!-- Footer -->
<footer class="py-3 bg-dark" id="footer">
    <div class="container">
        <h5 class="m-0 text-center text-white">Copyright @ qiruihua</h5>
    </div>
</footer>
</div>

<!-- 引入js -->
<script type="text/javascript" src="{% static 'js/host.js' %}"></script>
<script type="text/javascript" src="{% static 'js/common.js' %}"></script>
<script type="text/javascript" src="{% static 'js/index.js' %}"></script>
<script type="text/javascript" src="{% static 'js/jquery.pagination.min.js' %}"></script>
<script type="text/javascript">
    $(function () {
        $('#pagination').pagination({
            currentPage: {{page_num}},
            totalPage: {{total_page}},
            callback:function (current) {
<!--TODO:通过查询字符串分页跳转-->
                {# ?cat_id=3&page_size=10&page_num=2 #}
                location.href = '/?cat_id={{selected_category.id}}&page_size={{ page_size }}&page_num='+current;
            }
        })
    });
</script>
</body>
</html>
```

```python
from django.http.response import HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage


class IndexView(View):
    def get(self, request):
        # 1.后端获取数据库中分类信息
        categories = ArticleCategory.objects.all()
        # 2.浏览器从html接受用户点击的分类id
        cat_id = request.GET.get('cat_id', 1)  # 若html未传递，默认值1(从网页地址中取值)
        # 4.从html获取分页参数
        page_num = request.GET.get('page_num', 1)  # 目前页数，非总页数
        page_size = request.GET.get('page_size', 7)  # 单页对象数
        # 3.根据用户点击的分类id进行分类查询
        try:
            selected_category = ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('未在数据库中找到此文类ArticleCategory not found！！')
        # 5.获取分类信息筛选文章数据
        filtered_articles = Article.objects.filter(category=selected_category)  # 注意这里是对象
        # 6.创建分页器
        # (self, object_list, per_page, orphans=0,allow_empty_first_page=True)

        paginator = Paginator(filtered_articles, per_page=page_size)
        # 7.进行分页处理
        try:
            page_articles = paginator.page(page_num)
        except EmptyPage:
            return HttpResponseNotFound('empty page!')
        # 8.获取总页数
        total_page_num = paginator.num_pages
        # 8.组织数据传递给模板.html
        context = {
            # 分类参数
            'categories': categories,
            'selected_category': selected_category,
            # 分页参数
            'articles': page_articles,
            'page_size': page_size,
            'page_num': page_num,
            'total_page': total_page_num
        }
        return render(request, 'index.html', context=context)
```

