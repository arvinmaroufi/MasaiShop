from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin


@admin.register(models.SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['phone1', 'phone2', 'email1', 'email2', 'copy_right', 'instagram_link', 'telegram_link']


@admin.register(models.ContactUs)
class ContactUsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'short_message', 'get_date_send_jalali']

    def short_message(self, obj):
        if len(obj.message) > 20:
            return obj.message[:20] + '...'
        return obj.message
    short_message.short_description = 'متن پیام'

    @admin.display(description='تاریخ ارسال', ordering='date_send')
    def get_date_send_jalali(self, obj):
        return datetime2jalali(obj.date_send).strftime('%a, %d %b %Y')
