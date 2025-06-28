from django.urls import path
from . import views


app_name = 'dashboard'
urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.order_list, name='orders'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),
    path('orders_delivered/', views.orders_delivered, name='orders_delivered'),
    path('cart_summary/', views.cart_summary, name='cart_summary'),
    path('orders_cancelled/', views.orders_cancelled, name='orders_cancelled'),
]