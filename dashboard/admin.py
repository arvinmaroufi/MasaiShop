from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin


@admin.register(models.Address)
class AddressAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['user', 'title', 'short_full_address', 'city', 'province', 'postal_code', 'receiver_name',
                    'phone_number', 'is_default', 'get_created_at_jalali', 'get_updated_at_jalali']
    list_editable = ['is_default']

    def short_full_address(self, obj):
        if len(obj.full_address) > 20:
            return obj.full_address[:20] + '...'
        return obj.full_address
    short_full_address.short_description = 'آدرس کامل'

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a, %d %b %Y')

    @admin.display(description='تاریخ به‌روزرسانی', ordering='updated_at')
    def get_updated_at_jalali(self, obj):
        return datetime2jalali(obj.updated_at).strftime('%a, %d %b %Y')
