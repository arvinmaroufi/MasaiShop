from django.urls import path
from . import views


app_name = 'cart'
urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('shopping_payment/', views.shopping_payment, name='shopping_payment'),
    path('successful_payment/', views.successful_payment, name='successful_payment'),
]
