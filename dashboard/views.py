from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from cart.models import Order, CartItem, Cart
from product.models import Product, ProductComment
from django.core.paginator import Paginator


def get_pages_to_show(current_page, total_pages):
    if total_pages <= 3:
        return list(range(1, total_pages + 1))

    if current_page <= 2:
        return [1, 2, 3, '...', total_pages]

    if current_page >= total_pages - 1:
        return [1, '...', total_pages - 2, total_pages - 1, total_pages]

    return [1, '...', current_page - 1, current_page, current_page + 1, '...', total_pages]


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


@login_required
def order_list(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    orders = Order.objects.filter(user=user).order_by('-created_at')

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(orders, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'profile': profile,

        'orders': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'dashboard/orders.html', context)


@login_required
def order_detail(request, order_number):
    user = request.user
    profile = Profile.objects.get(user=user)
    order = get_object_or_404(Order, order_number=order_number, user=user)

    items = []
    for item_data in (order.items_data or []):
        try:
            product = Product.objects.get(pk=item_data['product_id'])
            item_data['product_obj'] = product
            items.append(item_data)
        except Product.DoesNotExist:
            continue

    context = {
        'profile': profile,

        'order': order,
        'items': items,
    }
    return render(request, 'dashboard/order_detail.html', context)


@login_required
def orders_delivered(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    orders = Order.objects.filter(user=user, status='delivered').order_by('-created_at')

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(orders, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'profile': profile,

        'orders': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'dashboard/orders_delivered.html', context)


@login_required
def cart_summary(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = cart.items.all()

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(cart_items, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'profile': profile,

        'cart_items': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'dashboard/cart_summary.html', context)


@login_required
def orders_cancelled(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    orders = Order.objects.filter(user=user, status='cancelled').order_by('-created_at')

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(orders, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'profile': profile,

        'orders': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'dashboard/orders_cancelled.html', context)