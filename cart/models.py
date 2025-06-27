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
        verbose_name_plural = 'کوپن ‌های تخفیف'

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


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='کاربر')
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='کوپن تخفیف')
    coupon_discount = models.IntegerField(default=0, verbose_name='مقدار تخفیف اعمال شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'

    def __str__(self):
        return f"سبد خرید {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def final_price(self):
        return self.total_price - self.coupon_discount

    def clear(self):
        self.items.all().delete()
        self.coupon = None
        self.coupon_discount = 0
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    color = models.ForeignKey(ProductColor, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='رنگ انتخاب شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم‌ های سبد خرید'
        unique_together = ['cart', 'product', 'color']

    def __str__(self):
        return f"{self.product.title} ({self.quantity})"

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    order_number = ShortUUIDField(length=10, max_length=10, alphabet="1234567890", unique=True, verbose_name="شماره سفارش")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name='آدرس')
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='سبد خرید')
    items_data = models.JSONField(null=True, blank=True, verbose_name='اطلاعات محصولات')
    total_price = models.IntegerField(verbose_name='مبلغ کل')
    coupon_discount = models.IntegerField(default=0, verbose_name='تخفیف کوپن')
    shipping_cost = models.IntegerField(default=0, verbose_name='هزینه ارسال')
    final_price = models.IntegerField(verbose_name='مبلغ قابل پرداخت')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending', verbose_name='وضعیت سفارش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        ordering = ['-created_at']

    def __str__(self):
        return f"سفارش {self.order_number} - {self.user.username}"

    def save(self, *args, **kwargs):
        if self.cart and not self.items_data:
            self.items_data = {
                'items': [{
                    'product': item.product.id,
                    'title': item.product.title,
                    'quantity': item.quantity,
                    'price': item.product.price
                } for item in self.cart.items.all()],
                'coupon': self.cart.coupon.code if self.cart.coupon else None,
                'discount': self.cart.coupon_discount
            }
        super().save(*args, **kwargs)
