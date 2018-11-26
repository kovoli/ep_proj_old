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


class Shop(models.Model):
    name = models.CharField(max_length=100)
    image_store = ProcessedImageField(upload_to='shop_image/',
                                      blank=True,
                                      processors=[Resize(200, 200)],
                                      format='JPEG',
                                      options={'quality': 80})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class Price(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    oldprice = models.DecimalField(decimal_places=2, max_digits=10)
    name = models.CharField(max_length=255)
    url = models.URLField()
    sales_notes = models.CharField(max_length=255, blank=True, null=True)
    # relate_models
    shop = models.ForeignKey(Shop, related_name='shop_prices', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    create = models.DateTimeField(auto_now=True)
    description = RichTextField(blank=True, null=True)
    characteristic = JSONField(blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    barcode = models.CharField(max_length=30, blank=True, null=True)
    vendorCode = models.CharField(max_length=50, blank=True, null=True)
    # relate_models
    category = TreeForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    prices = models.ForeignKey(Price, related_name='product_prices', on_delete=models.CASCADE,null=True, blank=True)

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [models.Index(fields=['name', 'slug'])]




