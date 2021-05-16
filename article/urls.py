from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('article-list/', views.article_list, name='article_list'),
    # 文章详情
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    # 用户写文章
    path('article-create/', views.article_create, name='article_create'),
    # 用户删文章
    path('article-delete/<int:id>', views.article_delete, name='article_delete'),
    path('article-safe-delete/<int:id>', views.article_safe_delete, name='article_safe_delete'),
    path('article-update/<int:id>', views.article_update, name='article_update'),
    # 类视图详情页
    # path('article-view/<int:pk>', views.ArticleDetailView.as_view(), name='...'),
    # 类视图创建文章页
    # path('create-view/', views.ArticleCreateView.as_view(), name='...'),
]
