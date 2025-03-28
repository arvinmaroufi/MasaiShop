from core.models import SiteSettings


def shop_func(request):
    site_settings = SiteSettings.objects.first()
    return {
        'site_settings': site_settings,
    }

