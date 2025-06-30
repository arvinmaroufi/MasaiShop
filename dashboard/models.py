from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from product.models import Product
from django.utils import timezone


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='کاربر')
    title = models.CharField(max_length=100, verbose_name='عنوان آدرس')
    full_address = models.TextField(max_length=300, verbose_name='آدرس کامل')
    city = models.CharField(max_length=50, verbose_name='شهر')
    province = models.CharField(max_length=50, verbose_name='استان')
    postal_code = models.CharField(max_length=10, validators=[RegexValidator(regex='^\d{10}$', message='کد پستی باید 10 رقم باشد')], verbose_name='کد پستی')

    receiver_name = models.CharField(max_length=100, verbose_name='نام تحویل گیرنده')
    phone_number = models.CharField(max_length=11, validators=[RegexValidator(regex='^09\d{9}$', message='شماره موبایل باید با 09 شروع شده و 11 رقم باشد')], verbose_name='شماره موبایل')

    is_default = models.BooleanField(default=False, verbose_name='آدرس پیش‌فرض')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس‌ ها'

    def __str__(self):
        return f"{self.title} - {self.receiver_name} ({self.city})"

    def save(self, *args, **kwargs):
        if self.is_default:
            self.user.addresses.exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists', verbose_name='محصول مربوطه')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'لیست علاقه ‌مندی'
        verbose_name_plural = 'لیست‌ های علاقه ‌مندی'
        unique_together = ('user', 'product')

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    message = models.TextField(verbose_name='پیام')
    is_for_all_users = models.BooleanField(default=False, help_text='با فعال‌سازی، اعلان به همه کاربران ارسال می‌شود', verbose_name='برای همه کاربران')
    users = models.ManyToManyField(User, blank=True, related_name='notifications', help_text='لیست کاربرانی که این اعلان را دریافت می‌کنند', verbose_name='کاربران هدف')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')
    expiration_date = models.DateTimeField(null=True, blank=True, help_text='تاریخی که پس از آن اعلان به صورت خودکار حذف خواهد شد', verbose_name='تاریخ انقضا')

    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلان‌ ها'
        ordering = ['-created_at']

    def __str__(self):
        return self.message

    @classmethod
    def delete_expired_notifications(cls):
        now = timezone.now()
        cls.objects.filter(models.Q(expiration_date__isnull=False) & models.Q(expiration_date__lt=now)).delete()
