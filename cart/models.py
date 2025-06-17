from django.db import models
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField
from product.models import Product, ProductColor
from dashboard.models import Address
from django.utils import timezone


class Coupon(models.Model):
    DISCOUNT_TYPE = (
        ('percentage', 'درصدی'),
        ('fixed', 'مبلغ ثابت')
    )

    code = models.CharField(max_length=20, unique=True, verbose_name='کد تخفیف')
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE, verbose_name='نوع تخفیف')
    discount_value = models.IntegerField(verbose_name='مقدار تخفیف')
    max_usage = models.IntegerField(null=True, blank=True, verbose_name='حداکثر استفاده')
    usage_count = models.IntegerField(default=0, verbose_name='تعداد استفاده شده')
    valid_from = models.DateTimeField(default=timezone.now, verbose_name='معتبر از')
    valid_to = models.DateTimeField(verbose_name='معتبر تا')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'کوپن تخفیف'
        verbose_name_plural = 'کوپن‌های تخفیف'

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.max_usage and self.usage_count >= self.max_usage:
            self.is_active = False
            self.save()
            return False
        if now < self.valid_from or now > self.valid_to:
            return False
        return True

