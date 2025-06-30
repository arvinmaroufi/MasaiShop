from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from cart.models import Order, CartItem, Cart
from product.models import Product, ProductComment
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from .models import Wishlist, Address, Notification
from .forms import AddressForm
from django.db.models import Q


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
    wishlist_products_count = Wishlist.objects.filter(user=user).count()

    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    popular_products = Product.objects.filter(status='published', stock_count__gt=0).order_by('-views')[:10]

    context = {
        'profile': profile,

        'current_cart_items': current_cart_items,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'comments_count': comments_count,
        'wishlist_products_count': wishlist_products_count,

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


@login_required
def orders_return(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        order_number = request.POST.get('order_number')

        try:
            order = Order.objects.get(order_number=order_number, user=user)

            if not profile.card_number:
                return JsonResponse({
                    'success': False,
                    'message': 'برای لغو سفارش باید شماره کارت خود را در پروفایل ثبت کنید.'
                })

            time_since_order = timezone.now() - order.created_at
            if time_since_order.total_seconds() > 48 * 3600:
                return JsonResponse({
                    'success': False,
                    'message': 'زمان لغو سفارش گذشته است. فقط تا 48 ساعت پس از ثبت سفارش امکان لغو وجود دارد.'
                })

            if order.status not in ['paid', 'shipped', 'pending']:
                return JsonResponse({
                    'success': False,
                    'message': 'این سفارش قابل لغو نیست. فقط سفارشات با وضعیت "پرداخت شده"، "ارسال شده" یا "در انتظار پرداخت" قابل لغو هستند.'
                })

            order.status = 'processing'
            order.save()

            return JsonResponse({
                'success': True,
                'message': 'سفارش شما در حال پردازش است. پس از تایید لغو سفارش، در بخش اعلان ها اطلاع خواهیم داد.'
            })

        except Order.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'سفارشی با این شماره یافت نشد.'
            })

    context = {
        'profile': profile,
    }
    return render(request, 'dashboard/orders_return.html', context)


@login_required
def wishlist_products(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    wishlist_items = Wishlist.objects.filter(user=user).select_related('product').order_by('-created_at')

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(wishlist_items, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'profile': profile,

        'wishlist_items': object_list,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'dashboard/wishlist_products.html', context)


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if created:
        message = "محصول به لیست علاقه ‌مندی‌ ها اضافه شد."
        status = 'success'
    else:
        message = "این محصول قبلاً در لیست علاقه‌ مندی‌ های شما وجود دارد."
        status = 'info'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status, 'message': message})
    return redirect('product:product_detail', pk=product_id)


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist_item = get_object_or_404(Wishlist, user=request.user, product=product)
    wishlist_item.delete()

    message = "محصول از لیست علاقه‌ مندی‌ ها حذف شد."
    status = 'success'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status, 'message': message})
    return redirect('dashboard:wishlist_products')


@login_required
def user_addresses(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    addresses = Address.objects.filter(user=user).order_by('-created_at')

    if request.method == 'POST':
        if 'delete_address' in request.POST:
            address_id = request.POST.get('delete_address')
            address = get_object_or_404(Address, pk=address_id, user=user)
            address.delete()
            return redirect('dashboard:user_addresses')

        if 'set_default' in request.POST:
            address_id = request.POST.get('set_default')
            address = get_object_or_404(Address, pk=address_id, user=user)
            address.is_default = True
            address.save()
            return redirect('dashboard:user_addresses')

        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = user
            address.save()
            return redirect('dashboard:user_addresses')
    else:
        form = AddressForm()

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(addresses, 6)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'profile': profile,

        'addresses': object_list,
        'form': form,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'dashboard/user_addresses.html', context)


@login_required
def notifications_list(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    Notification.delete_expired_notifications()

    now = timezone.now()
    notifications = Notification.objects.filter(
        is_active=True
    ).filter(
        Q(is_for_all_users=True) | Q(users=user)
    ).filter(
        Q(expiration_date__isnull=True) | Q(expiration_date__gte=now)
    ).distinct().order_by('-created_at')

    context = {
        'profile': profile,

        'notifications': notifications,
    }
    return render(request, 'dashboard/notifications_list.html', context)
