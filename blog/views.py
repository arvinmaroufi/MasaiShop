from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.core.paginator import Paginator


def get_pages_to_show(current_page, total_pages):
    if total_pages <= 3:
        return list(range(1, total_pages + 1))

    if current_page <= 2:
        return [1, 2, 3, '...', total_pages]

    if current_page >= total_pages - 1:
        return [1, '...', total_pages - 2, total_pages - 1, total_pages]

    return [1, '...', current_page - 1, current_page, current_page + 1, '...', total_pages]


def article_list(request):
    categories = Category.objects.all()
    articles = Article.objects.filter(status='published')
    latest_articles = Article.objects.filter(status='published').order_by('-created_at')[:6]

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 4)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'categories': categories,
        'articles': object_list,
        'latest_articles': latest_articles,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'blog/article_list.html', context)


def category_article(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()
    articles = category.articles.filter(status='published')
    latest_articles = Article.objects.filter(status='published').order_by('-created_at')[:6]

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 4)
    object_list = paginator.get_page(page_number)
    pages_to_show = get_pages_to_show(object_list.number, paginator.num_pages)

    context = {
        'category': category,
        'categories': categories,
        'articles': object_list,
        'latest_articles': latest_articles,
        'pages_to_show': pages_to_show,
    }
    return render(request, 'blog/category_article.html', context)

