from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class SiteSettings(models.Model):
    text_about_us = RichTextUploadingField(null=True, blank=True, verbose_name='متن درباره ما')
    text_contact_us = models.TextField(null=True, blank=True, verbose_name='متن تماس با ما')
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name='آدرس')
    phone1 = models.CharField(max_length=14, null=True, blank=True, verbose_name='شماره تلفن اول')
    phone2 = models.CharField(max_length=14, null=True, blank=True, verbose_name='شماره تلفن دوم')
    email1 = models.CharField(max_length=250, null=True, blank=True, verbose_name='ایمیل اول')
    email2 = models.CharField(max_length=250, null=True, blank=True, verbose_name='ایمیل دوم')
    copy_right = models.CharField(max_length=255, verbose_name='متن کپی رایت')
    instagram_link = models.CharField(max_length=250, null=True, blank=True, default='https://instagram.com/username', verbose_name='لینک اینستاگرام')
    telegram_link = models.CharField(max_length=250, null=True, blank=True, default='https://t.me/username', verbose_name='لینک تلگرام')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'


class ContactUs(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=14, verbose_name='شماره تماس')
    message = models.TextField(verbose_name='متن پیام')
    date_send = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')

    class Meta:
        ordering = ["-date_send"]
        verbose_name = "تماس با ما"
        verbose_name_plural = "تماس با ما"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
