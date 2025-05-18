from django.urls import path, re_path
from . import views


app_name = 'product'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    re_path(r'category/(?P<slug>[-\w]+)/', views.category_product_list, name='category_product_list'),
    re_path(r'brand/(?P<slug>[-\w]+)/', views.brand_product_list, name='brand_product_list'),
    path('discount_product/', views.discount_product_list, name='discount_product'),
    re_path(r'(?P<pid>[a-zA-Z0-9]+)/(?P<slug>[-\w]+)/', views.product_detail, name='product_detail'),
    path('product_search/', views.product_search, name='product_search'),
]
