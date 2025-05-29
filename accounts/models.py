from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام خانوادگی')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='ایمیل')
    about_me = models.CharField(max_length=250, null=True, blank=True, verbose_name='درباره من')
    phone = models.CharField(max_length=14, null=True, blank=True, verbose_name='شماره تلفن')
    postal_code = models.CharField(max_length=10, null=True, blank=True, verbose_name='کد پستی')
    image = models.ImageField(upload_to='profile/', null=True, blank=True, verbose_name='تصویر پروفایل')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'

    def __str__(self):
        return f"پروفایل {self.user.username}"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email
        )


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

