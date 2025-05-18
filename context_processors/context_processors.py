from core.models import SiteSettings
from product.models import ProductCategory, ProductColor, ProductBrand


def shop_func(request):
    site_settings = SiteSettings.objects.first()
    categories = ProductCategory.objects.all()
    colors = ProductColor.objects.all()
    brands = ProductBrand.objects.all()
    return {
        'site_settings': site_settings,
        'categories': categories,
        'colors': colors,
        'brands': brands,
    }

