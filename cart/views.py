from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Cart, CartItem, Coupon, Order
from product.models import Product, ProductColor
from dashboard.models import Address
from django.utils import timezone
import json


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    if not cart_items.exists() and cart.coupon:
        cart.coupon = None
        cart.coupon_discount = 0
        cart.save()

    total_price = sum(item.total_price for item in cart_items) if cart_items else 0
    shipping_cost = 50000 if total_price < 10500000 else 0
    final_price = total_price - cart.coupon_discount + shipping_cost

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'final_price': final_price,
    }
    return render(request, 'cart/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = get_object_or_404(Product, pk=product_id)
            color_id = data.get('color_id')
            quantity = int(data.get('quantity', 1))

            if quantity > product.stock_count:
                return JsonResponse({'success': False, 'message': 'تعداد درخواستی بیشتر از موجودی است'})

            cart, created = Cart.objects.get_or_create(user=request.user)

            if product.color.count() == 1:
                color = product.color.first()
            else:
                color = get_object_or_404(ProductColor, pk=color_id) if color_id else None

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                color=color,
                defaults={'quantity': quantity}
            )

            if not created:
                new_quantity = cart_item.quantity + quantity
                if new_quantity > product.stock_count:
                    return JsonResponse({'success': False, 'message': 'تعداد درخواستی بیشتر از موجودی است'})
                cart_item.quantity = new_quantity
                cart_item.save()

            return JsonResponse({'success': True, 'cart_count': cart.items.count()})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'درخواست نامعتبر'})


@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = data.get('quantity')
            color_id = data.get('color_id')

            cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)

            if color_id and str(color_id) != str(cart_item.color.id if cart_item.color else ''):
                new_color = get_object_or_404(ProductColor, pk=color_id)
                existing_item = CartItem.objects.filter(
                    cart=cart_item.cart,
                    product=cart_item.product,
                    color=new_color
                ).exclude(pk=cart_item.id).first()

                if existing_item:
                    existing_item.quantity += cart_item.quantity
                    existing_item.save()
                    cart_item.delete()
                    cart_item = existing_item
                else:
                    cart_item.color = new_color
                    cart_item.save()

            if quantity:
                quantity = int(quantity)
                if quantity > cart_item.product.stock_count:
                    return JsonResponse({'success': False, 'message': 'تعداد درخواستی بیشتر از موجودی است'})
                cart_item.quantity = quantity
                cart_item.save()

            cart = cart_item.cart
            total_price = sum(item.total_price for item in cart.items.all())
            shipping_cost = 50000 if total_price < 10500000 else 0
            final_price = total_price - cart.coupon_discount + shipping_cost

            return JsonResponse({
                'success': True,
                'item_price': cart_item.total_price,
                'total_price': total_price,
                'shipping_cost': shipping_cost,
                'final_price': final_price,
                'cart_count': cart.items.count()
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'درخواست نامعتبر'})


@login_required
def remove_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
            cart_item.delete()

            cart = Cart.objects.get(user=request.user)
            total_price = sum(item.total_price for item in cart.items.all())
            shipping_cost = 50000 if total_price < 10500000 else 0
            final_price = total_price - cart.coupon_discount + shipping_cost

            return JsonResponse({
                'success': True,
                'cart_count': cart.items.count(),
                'total_price': total_price,
                'shipping_cost': shipping_cost,
                'final_price': final_price
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'درخواست نامعتبر'})


@login_required
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            cart = Cart.objects.get(user=request.user)
            if not cart.items.exists():
                messages.error(request, 'سبد خرید شما خالی است')
                return redirect('cart:cart')

            coupon = Coupon.objects.get(code=coupon_code)
            if not coupon.is_valid():
                messages.error(request, 'کد تخفیف معتبر نیست یا منقضی شده است')
                return redirect('cart:cart')

            if cart.coupon:
                messages.warning(request, 'یک کد تخفیف قبلاً اعمال شده است')
                return redirect('cart:cart')

            total_price = sum(item.total_price for item in cart.items.all())

            if coupon.discount_type == 'percentage':
                discount = int((total_price * coupon.discount_value) / 100)
            else:
                discount = coupon.discount_value

            discount = min(discount, total_price)

            cart.coupon = coupon
            cart.coupon_discount = discount
            cart.save()

            coupon.usage_count += 1
            coupon.save()

            if coupon.max_usage and coupon.usage_count >= coupon.max_usage:
                coupon.is_active = False
                coupon.save()

            messages.success(request, f'کد تخفیف {coupon.code} با موفقیت اعمال شد ({discount:,} تومان تخفیف)')
        except Coupon.DoesNotExist:
            messages.error(request, 'کد تخفیف وارد شده معتبر نیست')
        return redirect('cart:cart')
    return redirect('cart:cart')


@login_required
def shopping_payment(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'سبد خرید شما خالی است')
        return redirect('cart:cart')

    default_address = Address.objects.filter(user=request.user, is_default=True).first()

    total_price = sum(item.total_price for item in cart.items.all())
    shipping_cost = 50000 if total_price < 10500000 else 0
    final_price = total_price - cart.coupon_discount + shipping_cost

    context = {
        'cart': cart,
        'default_address': default_address,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'final_price': final_price,
    }
    return render(request, 'cart/shopping_payment.html', context)

