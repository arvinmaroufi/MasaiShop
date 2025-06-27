from django.shortcuts import render, redirect
from .forms import ContactUsForm
from product.models import ProductBrand, Product
from django.db import models
from .models import Banner
from blog.models import Article


def home(request):
    # Banners
    main_sliders = Banner.objects.filter(banner_type='main_slider', status='published').order_by('-created_at')[:3]
    small_banners = Banner.objects.filter(banner_type='small_banner', status='published').order_by('-created_at')[:4]
    large_banners = Banner.objects.filter(banner_type='large_banner', status='published').order_by('-created_at')[:2]
    single_banner = Banner.objects.filter(banner_type='single_banner', status='published').order_by('-created_at').first()

    popular_brands = ProductBrand.objects.all().order_by('-views')[:10]
    popular_products = Product.objects.filter(status='published').order_by('-views')[:9]
    latest_products = Product.objects.filter(status='published', old_price=None).order_by('-created_at')[:4]
    latest_articles = Article.objects.filter(status='published').order_by('-created_at')[:5]
    discounted_products = Product.objects.filter(
        status='published', stock_count__gt=0,
        old_price__isnull=False,
        old_price__gt=models.F('price')
    ).annotate(
        discount=models.ExpressionWrapper(
            (models.F('old_price') - models.F('price')) * 100 / models.F('old_price'),
            output_field=models.IntegerField())).filter(discount__gt=0).order_by('-discount')[:8]
    best_selling_products = Product.objects.filter(status='published').order_by('-sales_count')[:7]

    context = {
        'main_sliders': main_sliders,
        'small_banners': small_banners,
        'large_banners': large_banners,
        'single_banner': single_banner,

        'popular_brands': popular_brands,
        'popular_products': popular_products,
        'latest_products': latest_products,
        'latest_articles': latest_articles,
        'discounted_products': discounted_products,
        'best_selling_products': best_selling_products,
    }
    return render(request, 'core/home.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    else:
        form = ContactUsForm()

    context = {
        'form': form
    }
    return render(request, 'core/contact.html', context)


def about(request):
    return render(request, 'core/about.html')
