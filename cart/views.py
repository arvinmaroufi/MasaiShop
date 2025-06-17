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

