from django.shortcuts import render

# 定义首页视图：
from django.views import View

# ------------------------
from home.models import ArticleCategory
from home.models import Article
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
        page_size = request.GET.get('page_size', 10)  # 单页对象数
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


# 定义详细页面(含显示，推荐，评论)视图：
from home.models import Article, ArticleCategory
from django.shortcuts import redirect  # 用于重定向
from django.urls import reverse  # 用于重定向
from home.models import Comment  # 用于入库


# -------------------------

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
