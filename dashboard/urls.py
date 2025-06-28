from django.urls import path
from . import views


app_name = 'dashboard'
urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.order_list, name='orders'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),
]