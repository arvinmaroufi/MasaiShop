from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.article_list, name='article_list'),
    re_path(r'category/(?P<slug>[-\w]+)/', views.category_article, name='article_category'),
]
