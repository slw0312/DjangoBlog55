from django import template
from django.db.models.aggregates import Count
from ..models import ArticlePost, ArticleColumn, TaggableManager

register = template.Library()


@register.inclusion_tag('article/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': ArticlePost.objects.dates('created', 'month', order='DESC'),
    }


@register.inclusion_tag('article/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = ArticleColumn.objects.annotate(num_posts=Count('article')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('article/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = ArticlePost.tags.all
    # .objects.annotate(num_posts=Count('article')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }


@register.simple_tag
def total_articles():
    # 返回文章对象总数
    return ArticlePost.objects.count()


@register.simple_tag
def total_tags():
    # 返回文章对象总数
    return ArticlePost.tags.count()


@register.simple_tag
def total_categories():
    # 返回文章对象总数
    return ArticleColumn.objects.count()
