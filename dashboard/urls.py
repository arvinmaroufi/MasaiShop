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
    path('orders_return/', views.orders_return, name='orders_return'),
    path('wishlist/', views.wishlist_products, name='wishlist_products'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('addresses/', views.user_addresses, name='user_addresses'),
    path('notifications/', views.notifications_list, name='notifications'),
    path('profile/', views.user_profile, name='user_profile'),
]
