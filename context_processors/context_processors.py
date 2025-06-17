from core.models import SiteSettings
from product.models import ProductCategory, ProductColor, ProductBrand
from cart.models import Cart, CartItem


def shop_func(request):
    site_settings = SiteSettings.objects.first()
    categories = ProductCategory.objects.all()
    colors = ProductColor.objects.all()
    brands = ProductBrand.objects.all()

    cart = None
    cart_items = []
    cart_total = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart_items = CartItem.objects.filter(cart=cart).select_related('product')
                cart_total = cart.total_price
        except:
            pass

    return {
        'site_settings': site_settings,
        'categories': categories,
        'colors': colors,
        'brands': brands,

        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }

