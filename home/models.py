from django.db import models
from django.utils import timezone  # 用于在分类创建时间中添加当前时间


# https://www.jb51.net/article/183845.htm

# Create your models here.

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
        verbose_name = '类别管理'  # admin站点显示
        verbose_name_plural = verbose_name  # 复数形式和单数一样
# -----------------------------------------------------------------

# 自定义文章模型：
from users.models import User  # 用于保存作者的外键
from django.utils import timezone # 用于保存创建时间，修改时间


class Article(models.Model):
    # 保存内容：作者，标题图，标题，分类，标签，摘要，正文，创建时间，浏览数，评论数，修改时间
    # ----------------------------------------------------------------------
    # 1.作者
    # (外键是用来连接两个表的键。一个外键是一个指向另一个表中的primary key的字段(或字段的集合),这里指向user信息
    # on_delete: 当user表中的数据删除后，文章信息中也同步删除（一致性确保）
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    # 2.标题图 #TODO:缺图测试
    avatar = models.ImageField(upload_to='article/%Y%m%d/',blank=True,null=True)
    # 3.标题
    title = models.CharField(max_length=20,blank=True)
    # 4.分类
    # related_name:和之前的_set操作的效果是一样的，这两个方法是相同的，所以如果觉得比较麻烦的话，可以在定义主表的外键的时候，直接就给外键定义好名称使用related_name
    # https://blog.csdn.net/hpu_yly_bj/article/details/78939748

    category = models.ForeignKey(ArticleCategory,null=True,blank=True,related_name='article',on_delete=models.CASCADE)
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
# ------------------------------------------------------------------
# 自定义评论模型：


class Comment(models.Model):
    # 保存内容：针对文章，用户名，时间，内容
    # -----------------------------------
    # 1.评论内容
    content = models.TextField(max_length=100)
    # 2.评论文章
    target_article = models.ForeignKey(Article,on_delete=models.SET_NULL,null=True)
    # 3.评论用户
    user = models.ForeignKey('users.User',on_delete=models.SET_NULL,null=True)
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