from django.contrib import admin

# Register your models here.
# 注册模型以供后台管理：

from home.models import ArticleCategory
from home.models import Article
from home.models import Comment
# 注册模型：
admin.site.register(ArticleCategory)
admin.site.register(Article)
admin.site.register(Comment)
