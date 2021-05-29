from django.shortcuts import render

# Create your views here.

from django.views import View

# 定义注册视图
from django.http.response import HttpResponseBadRequest
import re  # 用于正则表达式处理->2.2,2.3
from users.models import User  # 用于保存用户信息->3
from django.db import DatabaseError  # 用于异常处理
from django.shortcuts import redirect  # 用于重定向 ->5
from django.urls import reverse  # 用于重定向->5


class RegisterView(View):  # 继承自View

    def get(self, request):
        return render(request, 'register.html')  # 返回一个网页，由.html渲染

    # 实现注册功能：
    # get/post区别： https://www.cnblogs.com/zhansheng/p/11823689.html)
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
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)  # 此即为注册的用户,用户名初始为手机号
        except DatabaseError as e:
            logger.error(e)
            return HttpResponseBadRequest('注册失败！')
        # 4.注册后状态保持（免登录）
        from django.contrib.auth import login
        login(request, user)
        # 5.返回响应跳转到指定页面
        # TODO: 暂时返回一个注册成功信息，以后实现跳转到指定页面。2021.5.2
        # return HttpResponse('注册成功，重定向到首页。')

        # redirect() 可以进行重定向
        # reverse() 可以通过namespace:name 来获取视图对应的路由
        # return redirect(reverse('home:index'))
        # cookie需要到response中设置
        response = redirect(reverse('home:index'))
        # 设置2个cookie信息（会话结束后自动过期），以方便首页中用户信息展示的判断和用户信息的展示 (自动登录)
        response.set_cookie('is_login', True)  # 展示
        response.set_cookie('username', user.username, max_age=7 * 24 * 3600)
        return response


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
            return HttpResponseBadRequest('UUID传递失败！要在imagecode/后输入?uuid= xxx  :p貌似存进去了')
        # 3.通过调用Captcha来生成图片验证码（图片二进制，图片内容）
        text, image = captcha.generate_captcha()
        # 4.保存图片内容至redis（以uuid为key，图片内容为value，还要设置一个时效）
        redis_conn = get_redis_connection('default')  # 0号库

        # RedisSetex命令为指定的key设置值及其过期时间。如果key已经存在， SETEX命令将会替换旧的值。
        # https://www.runoob.com/redis/strings-setex.html
        # key设置为 UUID ,添加一个前缀
        # seconds 过期秒数300秒（5分）
        # value 图片二进制内容text
        redis_conn.setex('img:%s' % uuid, 300, text)
        # 5.返回图片二进制 （注意因为返回的是图片，要告知返回类型）
        return HttpResponse(image, content_type='image/jpeg')


# 定义短信验证码视图：
from django.http.response import JsonResponse  # 用于网页实时报错->2.1
from utils.response_code import RETCODE  # 用于->2.1
import logging  # 用于->2.2.3,3.1:异常处理记录
from random import randint  # 用于->3.1 生成随机验证码

logger = logging.getLogger('django')
from libs.yuntongxun.sms import CCP  # 用于发送验证短信->5


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

        CCP().send_template_sms(mobile, [sms_code, 5], 1)

        # 6.返回响应
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '短信验证码发送成功！'})


# 定义登录视图：
from django.contrib.auth import login  # 用于登录、状态保持->4
from django.contrib.auth import authenticate  # 用于验证登录信息->3


# 用于默认认证方法：针对username字段进行用户名的判断


class LoginView(View):
    # 因为是在浏览器中获取登录页面：
    def get(self, request):
        return render(request, 'login.html')

    # 登录功能实现（业务逻辑）
    def post(self, request):
        # 1.接收参数
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        # 2.参数验证
        # 2.1验证手机号
        if not re.match(r'^1[3-9]\d{9}$', mobile):  # \d匹配一个数字字符。等价于[0-9]。
            return HttpResponseBadRequest('手机号格式不符合规则:D')
        # 2.1验证密码
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return HttpResponseBadRequest('输入的密码不符合规则:D：8-20位非符号字符')
        # 3.用户认证登录（采用系统自带的认证方法django.contrib.auth:authenticate()）
        # 3.1两者正确，返回库中的user:
        user = authenticate(mobile=mobile, password=password)  # 注意不是用username认证！
        # 3.2任一错误，返回None:
        if user is None:
            return HttpResponseBadRequest('用户名或密码错误,登陆失败！')
        # 4.状态保持
        login(request, user)
        # 5.根据用户选择是否记住登陆状态进行判断
        # 6.为了首页显示而设置一些cookie信息（配合remember）
        # response = redirect(reverse('home:index'))
        # extra: 根据mixin中next参数进行判断页面跳转：
        next_page = request.GET.get('next')  # 判断url中有没有这个关键字参数
        if next_page:  # 如果有：
            response = redirect(next_page)
        else:
            response = redirect(reverse('home:index'))
        # 5.1没记住：
        if remember != 'on':  # 说明没有记住用户信息
            request.session.set_expiry(0)  # 浏览器关闭之后
            # TODO:'TIME:0'改不得啊日了狗了debug半天
            response.set_cookie('is_login', True)
            response.set_cookie('username', user.username, max_age=14 * 24 * 3600)
        # 5.2记住了：
        else:
            request.session.set_expiry(None)  # None:默认两周
            response.set_cookie('is_login', True, max_age=14 * 24 * 3600)
            response.set_cookie('username', user.username, max_age=14 * 24 * 3600)

        # 7.返回响应
        return response


# 定义注销视图：
from django.contrib.auth import logout


class LogoutView(View):

    def get(self, request):
        # 1.session数据清除
        logout(request)
        # 2.cookie数据部分删除
        response = redirect(reverse('home:index'))
        response.delete_cookie('is_login')
        response.delete_cookie('username')
        # 3.跳转到首页
        return response


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


# 定义用户中心视图：

from django.contrib.auth.mixins import LoginRequiredMixin  # 混入扩展类，实际上还是调用了`request.user.is_authenticated()`


# 如果用户未登录，则进行默认跳转，默认跳转链接为：accounts/login/?next=/usercenter/,accounts/login/+查询字符串
# 前面的默认跳转链接可在root/settings.py中修改；next=/.../用于回跳


class UserCenterView(LoginRequiredMixin, View):
    def get(self, request):
        # 前端获得登录用户的信息：
        user = request.user
        # 前端组织获取用户信息：
        context = {
            'username': user.username,
            'mobile': user.mobile,
            # 如果头像存在的话获取头像，否则返回None
            'avatar': user.avatar.url if user.avatar else None,
            'user_desc': user.user_desc
        }
        return render(request, 'center.html', context=context)

    def post(self, request):
        # 业务逻辑：
        # 1.接收参数
        konouser = request.user
        update_username = request.POST.get('username', konouser.username)  # (如果没有传递的话还是用之前的用户信息)
        update_user_desc = request.POST.get('desc', konouser.user_desc)
        # 头像信息为ImageField（models.py），为file类型
        update_avatar = request.FILES.get('avatar')  # 保底判断在center.html里
        # 2.将参数保存入库
        try:
            konouser.username = update_username
            konouser.user_desc = update_user_desc
            if update_avatar:
                konouser.avatar = update_avatar
            konouser.save()  # 注意保存
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('修改失败！重新试试？')
        # 3.刷新当前页面（重定向）
        response = redirect(reverse('users:usercenter'))
        # 4.更新cookie中的username信息
        response.set_cookie('username', konouser.username, max_age=14 * 24 * 3600)
        # 5.返回响应
        return response


# 定义写文章视图：（回跳功能已经在RegisterView下实现）
from home.models import ArticleCategory  # 用于写博客页面展示文类
from home.models import Article


# 同样需要先登录才能写：
class WriteBlogView(LoginRequiredMixin, View):
    def get(self, request):
        # 查询所有分类模型
        categories = ArticleCategory.objects.all()

        context = {
            'categories': categories
        }
        return render(request, 'write_blog.html', context=context)

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
        # 2.1参数是否齐全#TODO:缺图测试
        if not all([ title, category_id, summary, content]):
            return HttpResponseBadRequest('参数没写全，不收录！-へ-')
            # 2.2分类id判断
        try:
            confirm_category_obj = ArticleCategory.objects.get(id=category_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseBadRequest('没有此分类哦~')
        # 3.保存入库
        try:
            article = Article.objects.create(
                title=title,    # 测试下来不能带符号如：！
                author=author,
                avatar=avatar,
                category=confirm_category_obj,
                tags=tags,
                summary=summary,
                content=content
            )
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('数据库相关错误，无法发布orz，注意title不能带符号')
        # 4.跳转
        response = redirect(reverse('home:index'))
        # 5.返回响应
        return response
