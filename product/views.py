from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductComment, ProductCategory, ProductBrand, ProductColor
from django.db import models
from django.core.paginator import Paginator
from django.db.models import Min, Max, Q
from urllib.parse import urlencode
from django.http import JsonResponse
from dashboard.models import Wishlist


def redirect_to_home(request):
    return redirect('core:home')


def get_pages_to_show(current_page, total_pages):
    if total_pages <= 3:
        return list(range(1, total_pages + 1))

    if current_page <= 2:
        return [1, 2, 3, '...', total_pages]

    if current_page >= total_pages - 1:
        return [1, '...', total_pages - 2, total_pages - 1, total_pages]

    return [1, '...', current_page - 1, current_page, current_page + 1, '...', total_pages]


def product_list(request):
    products = Product.objects.filter(status='published')

    # Filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    in_stock = request.GET.get('in_stock')

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    if in_stock == '1':
        products = products.filter(stock_count__gte=1)

    prices = Product.objects.filter(status='published').aggregate(min=Min('price'), max=Max('price'))

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(products, 9)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        'products': object_list,
        'pages_to_show': pages_to_show,
        'min_price': min_price or prices['min'],
        'max_price': max_price or prices['max'],
        'actual_min_price': prices['min'],
        'actual_max_price': prices['max'],
        'in_stock': in_stock,
        'querystring': urlencode(query_params)
    }
    return render(request, 'product/product_list.html', context)


def category_product_list(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    products = Product.objects.filter(status='published', category=category)

    # Filters
    selected_colors = request.GET.getlist('color')
    selected_brands = request.GET.getlist('brand')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    in_stock = request.GET.get('in_stock')

    if selected_colors:
        products = products.filter(color__id__in=selected_colors)

    if selected_brands:
        products = products.filter(brand__id__in=selected_brands)

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    if in_stock == '1':
        products = products.filter(stock_count__gte=1)

    products = products.distinct()

    prices = Product.objects.filter(status='published', category=category).aggregate(min=Min('price'), max=Max('price'))

    # Pagination
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        'category': category,
        'products': object_list,
        'colors': ProductColor.objects.all(),
        'brands': ProductBrand.objects.all(),
        'pages_to_show': pages_to_show,
        'selected_colors': list(map(int, selected_colors)),
        'selected_brands': list(map(int, selected_brands)),
        'min_price': min_price or prices['min'],
        'max_price': max_price or prices['max'],
        'actual_min_price': prices['min'],
        'actual_max_price': prices['max'],
        'in_stock': in_stock,
        'querystring': urlencode(query_params)
    }
    return render(request, 'product/category_product_list.html', context)


def brand_product_list(request, slug):
    brand = get_object_or_404(ProductBrand, slug=slug)
    products = Product.objects.filter(status='published', brand=brand)

    # Filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    in_stock = request.GET.get('in_stock')

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    if in_stock == '1':
        products = products.filter(stock_count__gte=1)

    prices = Product.objects.filter(status='published').aggregate(min=Min('price'), max=Max('price'))

    # Pagination
    paginator = Paginator(products.distinct(), 9)
    page_number = request.GET.get('page')
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        'brand': brand,
        'brands': ProductBrand.objects.all().order_by('-views')[:6],
        'products': object_list,
        'pages_to_show': pages_to_show,
        'min_price': min_price or prices['min'],
        'max_price': max_price or prices['max'],
        'actual_min_price': prices['min'],
        'actual_max_price': prices['max'],
        'in_stock': in_stock,
        'querystring': urlencode(query_params)
    }
    return render(request, 'product/brand_product_list.html', context)


def discount_product_list(request):
    products = Product.objects.filter(
        status='published',
        old_price__isnull=False,
        old_price__gt=models.F('price')
    ).annotate(
        discount=models.ExpressionWrapper(
            (models.F('old_price') - models.F('price')) * 100 / models.F('old_price'),
            output_field=models.IntegerField())).filter(discount__gt=0).order_by('-discount')

    # Filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    in_stock = request.GET.get('in_stock')

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    if in_stock == '1':
        products = products.filter(stock_count__gte=1)

    prices = Product.objects.filter(status='published').aggregate(min=Min('price'), max=Max('price'))

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(products, 9)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        'products': object_list,
        'min_price': min_price or prices['min'],
        'max_price': max_price or prices['max'],
        'actual_min_price': prices['min'],
        'actual_max_price': prices['max'],
        'in_stock': in_stock,
        'pages_to_show': pages_to_show,
        'querystring': urlencode(query_params)
    }
    return render(request, 'product/discount_product_list.html', context)


def product_detail(request, pid, slug):
    products = get_object_or_404(Product, pid=pid, slug=slug)
    product_image = products.product_images.all()

    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        import json
        data = json.loads(request.body)
        body = data.get('body')
        if request.user.is_authenticated and body:
            comment = ProductComment.objects.create(body=body, product=products, author=request.user)
            return JsonResponse({'status': 'success', 'comment_id': comment.id})
        return JsonResponse({'status': 'fail'}, status=400)

    comments = products.product_comments.filter(status='published').order_by('-created_at')

    viewed_products = request.session.get('viewed_products', [])
    if products.id not in viewed_products:
        products.views += 1
        products.save(update_fields=['views'])
        viewed_products.append(products.id)
        request.session['viewed_products'] = viewed_products

    is_in_wishlist = False
    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(user=request.user, product=products).exists()

    context = {
        'products': products,
        'product_image': product_image,
        'comments': comments,
        'is_in_wishlist': is_in_wishlist,
    }
    return render(request, 'product/product_detail.html', context)


def product_search(request):
    products_search = request.GET.get('search', '')
    products = Product.objects.filter(title__icontains=products_search, status='published')

    # Filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    in_stock = request.GET.get('in_stock')

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    if in_stock == '1':
        products = products.filter(stock_count__gte=1)

    prices = Product.objects.filter(status='published').aggregate(min=Min('price'), max=Max('price'))

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(products, 9)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    context = {
        'products': object_list,
        'pages_to_show': pages_to_show,
        'search': products_search,
        'min_price': min_price or prices['min'],
        'max_price': max_price or prices['max'],
        'actual_min_price': prices['min'],
        'actual_max_price': prices['max'],
        'in_stock': in_stock,
        'querystring': urlencode(query_params),
    }

    return render(request, 'product/product_list.html', context)
