from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from cart.models import Order, CartItem
from product.models import Product, ProductComment


@login_required
def home(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    # User account statistics
    current_cart_items = CartItem.objects.filter(cart__user=user).count()
    delivered_orders = Order.objects.filter(user=user, status='delivered').count()
    cancelled_orders = Order.objects.filter(user=user, status='cancelled').count()
    comments_count = ProductComment.objects.filter(author=user).count()

    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    popular_products = Product.objects.filter(status='published', stock_count__gt=0).order_by('-views')[:10]

    context = {
        'profile': profile,

        'current_cart_items': current_cart_items,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'comments_count': comments_count,

        'recent_orders': recent_orders,
        'popular_products': popular_products,
    }
    return render(request, 'dashboard/home.html', context)