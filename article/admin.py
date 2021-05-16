from django.contrib import admin
from .models import ArticlePost,ArticleColumn
# Register your models here.

# 注册ArticlePost到admin中
admin.site.register(ArticlePost)
admin.site.register(ArticleColumn)