from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin


@admin.register(models.Category)
class CategoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title', 'get_created_jalali']
    prepopulated_fields = {'slug': ('title',)}

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a, %d %b %Y')


@admin.register(models.Article)
class ArticleAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['short_title', 'author', 'views', 'article_image', 'get_created_jalali', 'status']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']

    def short_title(self, obj):
        if len(obj.title) > 20:
            return obj.title[:20] + '...'
        return obj.title
    short_title.short_description = 'عنوان مقاله'

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a, %d %b %Y')


