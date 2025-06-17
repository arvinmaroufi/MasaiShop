from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import format_html
from shortuuid.django_fields import ShortUUIDField


STATUS = (
    ("draft", "پیش نویس شود"),
    ("published", "منتشر شود")
)


class ProductCategory(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='نامک')
    image = models.ImageField(upload_to='images/products/categories', null=True, blank=True, verbose_name='تصویر دسته بندی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def category_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="50px" height="50px">')
        return format_html(f'<h3 style="color: red">تصویر ندارد</h3>')

    def __str__(self):
        return self.title


class ProductBrand(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان برند')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='نامک')
    image = models.ImageField(upload_to='images/brands', null=True, blank=True, verbose_name='تصویر برند')
    views = models.IntegerField(default=0, verbose_name='بازدید ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def brand_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="50px" height="50px">')
        return format_html(f'<h3 style="color: red">تصویر ندارد</h3>')

    def __str__(self):
        return self.title


class ProductColor(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='عنوان رنگ')
    color_code = models.CharField(max_length=20, unique=True, default="#000000", help_text='این یک کد رنگی پیش فرض است', verbose_name='کد رنگ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345", verbose_name="شناسه محصول")
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='فروشنده')
    category = models.ManyToManyField(ProductCategory, related_name='categories', verbose_name='دسته بندی مربوطه')
    title = models.CharField(max_length=300, unique=True, verbose_name='عنوان محصول')
    slug = models.SlugField(max_length=300, unique=True, allow_unicode=True, verbose_name='نامک')
    description = RichTextUploadingField(verbose_name='توضیحات تکمیلی')
    old_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت قدیمی محصول')
    price = models.IntegerField(verbose_name='قیمت محصول')
    stock_count = models.IntegerField(verbose_name='تعداد موجود')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    status = models.CharField(choices=STATUS, max_length=10, default='published', verbose_name='وضعیت')
    views = models.IntegerField(default=0, verbose_name='بازدید ها')
    sales_count = models.IntegerField(default=0, verbose_name='تعداد فروش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    # General Features
    brand = models.ManyToManyField(ProductBrand, related_name='product_brands', null=True, blank=True, verbose_name='برند مربوطه')
    model = models.CharField(max_length=100, blank=True, null=True, verbose_name='مدل')
    color = models.ManyToManyField(ProductColor, null=True, blank=True, related_name='colors', verbose_name='رنگ')
    weight = models.CharField(max_length=50, blank=True, null=True, verbose_name='وزن')
    dimensions = models.CharField(max_length=100, blank=True, null=True, verbose_name='ابعاد')
    # Special Features for Products
    operating_system = models.CharField(max_length=50, blank=True, null=True, verbose_name='سیستم عامل')
    battery_capacity = models.CharField(max_length=50, blank=True, null=True, verbose_name='ظرفیت باتری')
    ram = models.CharField(max_length=50, blank=True, null=True, verbose_name='حافظه موقت')
    internal_memory = models.CharField(max_length=50, blank=True, null=True, verbose_name='حافظه داخلی')
    camera_resolution = models.CharField(max_length=50, blank=True, null=True, verbose_name='رزولوشن دوربین')
    connectivity = models.CharField(max_length=100, blank=True, null=True, verbose_name='نوع اتصال')
    processor_generation = models.CharField(max_length=50, blank=True, null=True, verbose_name='نسل پردازنده')
    processor_manufacturer = models.CharField(max_length=50, blank=True, null=True, verbose_name='سازنده پردازنده')
    processor_series = models.CharField(max_length=50, blank=True, null=True, verbose_name='سری پردازنده')
    body_material = models.CharField(max_length=50, blank=True, null=True, verbose_name='جنس بدنه')
    strap_material = models.CharField(max_length=50, blank=True, null=True, verbose_name='جنس بند')
    display_size = models.CharField(max_length=50, blank=True, null=True, verbose_name='اندازه صفحه نمایش')
    bluetooth_version = models.CharField(max_length=50, blank=True, null=True, verbose_name='نسخه بلوتوث')
    antenna_count = models.CharField(max_length=50, null=True, blank=True, verbose_name='تعداد آنتن')
    antenna_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='نوع آنتن')
    power_source = models.CharField(max_length=50, blank=True, null=True, verbose_name='منبع تغذیه')
    os_support = models.TextField(blank=True, null=True, verbose_name='قابلیت پشتیبانی از سیستم عامل‌های')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def discount_percentage(self):
        if self.old_price and self.price < self.old_price:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return int(discount) if discount > 0 else None
        return 0

    def product_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="50px" height="50px">')
        return format_html(f'<h3 style="color: red">تصویر ندارد</h3>')

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="product_images", on_delete=models.CASCADE, verbose_name="محصول")
    images = models.ImageField(upload_to='images/products/product_images', verbose_name="تصاویر محصولات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصولات"

    def __str__(self):
        return self.product.title


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments', verbose_name='محصول مربوطه')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_comments', verbose_name='نویسنده دیدگاه')
    body = models.TextField(verbose_name='متن دیدگاه')
    status = models.CharField(choices=STATUS, max_length=10, default='published', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return self.product.title

