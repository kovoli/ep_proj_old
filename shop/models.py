from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# for slugfield
from django.urls import reverse
from django.template.defaultfilters import slugify
from unidecode import unidecode

from ckeditor.fields import RichTextField
# Images
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Resize, ResizeCanvas, ResizeToFill, ResizeToCover, ResizeToFit, SmartResize

from django.contrib.postgres.fields import JSONField


# ----------- CATEGORY -------------
class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = RichTextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category', args=[self.slug])

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# -------------- SHOP ---------------
class Shop(models.Model):
    name = models.CharField(max_length=100)
    image_store = ProcessedImageField(upload_to='shop_image/',
                                      blank=True,
                                      processors=[ResizeToFit(200, 200)],
                                      format='JPEG',
                                      options={'quality': 80})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


# ------------ VENDOR ---------------
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image_vendor = ProcessedImageField(upload_to='vendor_image/',
                                       blank=True,
                                       processors=[ResizeToFit(200, 200)],
                                       format='JPEG',
                                       options={'quality': 80})

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:vendor', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Vendor, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


# ------------ PRODUCT -------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    create = models.DateTimeField(auto_now=True)
    description = RichTextField(blank=True, null=True)
    characteristic = JSONField(blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    barcode = models.CharField(max_length=30, blank=True, null=True)
    vendorCode = models.CharField(max_length=50, blank=True, null=True)
    product_image = ProcessedImageField(upload_to='product_images/%Y/%m',
                                        processors=[ResizeToFit(None, 350)],
                                        format='JPEG',
                                        options={'quality': 80},
                                        blank=True,
                                        max_length=250)
    # related_models
    category = TreeForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey('Vendor', related_name='vendors', on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [models.Index(fields=['name', 'slug'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Product, self).save(*args, **kwargs)


# ------------ PRICE --------------
class Price(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    oldprice = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    sales_notes = models.CharField(max_length=255, blank=True, null=True)
    # relate_models
    shop = models.ForeignKey(Shop, related_name='shop_prices', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
        indexes = [models.Index(fields=['product', 'shop'])]

