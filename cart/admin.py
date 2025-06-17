from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin


@admin.register(models.Coupon)
class CouponAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'max_usage', 'usage_count',
                    'get_valid_from_jalali', 'get_valid_to_jalali', 'is_active']
    list_editable = ['is_active']

    @admin.display(description='معتبر از', ordering='valid_from')
    def get_valid_from_jalali(self, obj):
        return datetime2jalali(obj.valid_from).strftime('%a, %d %b %Y')

    @admin.display(description='معتبر تا', ordering='valid_to')
    def get_valid_to_jalali(self, obj):
        return datetime2jalali(obj.valid_to).strftime('%a, %d %b %Y')


@admin.register(models.Cart)
class CartAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['user', 'coupon', 'coupon_discount', 'get_created_at_jalali', 'get_updated_at_jalali']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a, %d %b %Y')

    @admin.display(description='تاریخ به‌روزرسانی', ordering='updated_at')
    def get_updated_at_jalali(self, obj):
        return datetime2jalali(obj.updated_at).strftime('%a, %d %b %Y')

