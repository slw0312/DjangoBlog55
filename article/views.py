from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ArticlePost
import markdown
# 引入AriticlePostForm表单类
from .form import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User


# Create your views here.
def article_list(request):
    # 取出所有博客文章
    articles = ArticlePost.objects.all()
    # 需要传递给模板（templates）的对象
    context = {'articles': articles}
    # render函数：载入模板，并返回context对象
    return render(request, 'list.html', context)


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body, extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
    ])

    # 需要传递给模板的对象
    context = {'article': article}
    # 载入模板，并返回context对象
    return render(request, 'detail.html', context)


# 用户文章视图
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中id=1的用户为作者
            # 如果进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=1)
            # 将文章保存到数据库中
            new_article.save()
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
        context = {'article_post_form': article_post_form}
        return render(request, 'create.html')


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
def article_update(request, id):
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 判断用户是否为POST提交表单数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的title、body数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的id值
            return redirect('article:article_detail', id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    # 如果用户GET请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将article文章对象也传递进去，以便提取旧的内容
        context = {'article': article}
        # 将响应返回到模板中
        return render(request, 'update.html', context)

