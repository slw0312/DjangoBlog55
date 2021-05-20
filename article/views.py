from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from .models import ArticlePost, ArticleColumn
import markdown
# 引入AriticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
# 引入验证登录的装饰器
from django.contrib.auth.decorators import login_required
# 引入分页模块
from django.core.paginator import Paginator
# 引入Q对象
from django.db.models import Q
# 引入comment模型
from comment.models import Comment
# 引入第三方库pure_pagination的分页混入类
from pure_pagination.mixins import PaginationMixin
# 引入用户扩展信息模型
from userprofile.models import Profile
# Django-taggit
from taggit.managers import TaggableManager

from django.views.generic import ListView


# Create your views here.
# 首页类视图
class IndexView(PaginationMixin, ListView):
    model = ArticlePost
    template_name = 'index.html'  # 指定模板
    context_object_name = 'post_list'  # 指定获取的模型列表数据保存的变量名，这个变量会被传递给模板。
    paginate_by = 10  # 每页文章数


# TODO:此处为about页面临时视图，将其放到合适的地方
def about(request):
    return render(request, 'about.html')


# TODO:此处为single-post(detail)页面临时视图。
def single_post(request):
    return render(request, 'homeplate/single-post.html')


# TODO：直接命名为首页视图
# 文章列表视图
def article_list(request):
    # # 取出所有博客文章
    # articles = ArticlePost.objects.all()
    # article_list = ArticlePost.objects.all()
    # # 每页显示一篇文章
    # paginator = Paginator(article_list, 3)
    # # 取出url中的页码
    # '''在GET请求中，在url的末尾附上?key=value的键值对，视图中就可以通过request.GET.get('key')来查询value的值'''
    # page = request.GET.get('page')
    # # 将导航对象相应的页码内容返回给 articles
    # articles = paginator.get_page(page)
    # # 需要传递给模板（templates）的对象
    # context = {'articles': articles}
    # 根据GET请求中查询条件返回不同排序的对象数组
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    # 初始化查询集
    article_list = ArticlePost.objects.all()
    # 用户搜索逻辑
    if search:
        if order == 'total_views':
            # 用Q对象，进行联合搜索
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    # TODO:更加复杂、深度定制的搜索.借助第三方模块，如Haystack
    else:
        # 将 search 参数重置为空
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()
    # if request.GET.get('order') == 'total_views':
    #     article_list = ArticlePost.objects.all().order_by('-total_views')
    #     order = 'total_views'
    # else:
    #     article_list = ArticlePost.objects.all()
    #     order = 'normal'
    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)
    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])
    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 博主扩展信息
    profile = Profile.objects.get(id=1)
    # user = User.objects.get(is_superuser=1)

    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
        'profile': profile,
    }
    # render函数：载入模板，并返回context对象
    return render(request, 'index.html', context)
    # return render(request, 'list.html', context)


# 分类
def category(request, pk):
    cate = get_object_or_404(ArticleColumn, pk=pk)
    articles = ArticlePost.objects.filter(column=cate).order_by('-created')
    return render(request, 'index.html', context={'articles': articles})


# 标签
def tag(request, pk):
    t = get_object_or_404(TaggableManager, pk=pk)
    articles = ArticlePost.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'index.html', context={'articles': articles})


# 归档
def archive(request, year, month):
    articles = ArticlePost.objects.filter(
        created__year=year,
        created__month=month).order_by('-created')
    return render(request, 'index.html', context={'articles': articles})


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 取出文章评论
    comments = Comment.objects.filter(article=id)  # 取出多个满足条件的对象
    # 浏览量+1
    article.total_views += 1
    article.save(update_fields=['total_views'])  # update_fields=[]指定了数据库只更新total_views字段
    # 将markdown语法渲染成html样式
    # article.body = markdown.markdown(article.body, extensions=[
    #     # 包含 缩写、表格等常用扩展
    #     'markdown.extensions.extra',
    #     # 语法高亮扩展
    #     'markdown.extensions.codehilite',
    #     # 目录扩展
    #     'markdown.extensions.TOC'
    # ])
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc'
        ]
    )
    # 将 article.body 中的 Markdown 文本解析成 HTML 文本
    article.body = md.convert(article.body)

    # 需要传递给模板的对象
    context = {'article': article, 'toc': md.toc, 'comments': comments}
    # 载入模板，并返回context对象
    return render(request, 'single-post.html', context)
    # return render(request, 'detail.html', context)


# 用户文章视图
@login_required(login_url='userprofile/login/')  # 检查登录
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定目前登录的用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            # 若上传了文章介绍图，则赋值
            if 'introduce' in request.FILES:
                new_article.introduce = new_article['introduce']
            # 将文章保存到数据库中
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()
            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect('article:article_list')
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns}
        return render(request, 'create.html')


# TODO:article_delete&article_update(ok) need verification
# 删除文章
def article_delete(request, id):
    # 根据id获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用delete()方法删除文章
    article.delete()
    # 完成后返回文章列表
    return redirect('article:article_list')


# 安全删除文章
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅允许post请求')


# 更新文章
@login_required(login_url='urserprofilr/login/')  # 过滤未登录的用户,提醒用户登录
def article_update(request, id):
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse('抱歉，你无权修改这篇文章。')
    # 判断用户是否为POST提交表单数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的title、body数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的id值
            # request.session['id'] = id
            return redirect('article:article_detail', id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    # 如果用户GET请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将article文章对象也传递进去，以便提取旧的内容
        columns = ArticleColumn.objects.all()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
        }
        # 将响应返回到模板中
        return render(request, 'update.html', context)
