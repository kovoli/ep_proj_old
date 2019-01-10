from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.urls import reverse
from django.template.defaultfilters import slugify
from unidecode import unidecode
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField


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
        return reverse('discounts:discount_category_catalog', args=[self.slug])

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['-name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [models.Index(fields=['slug'])]


# ------------ VENDOR ---------------
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Vendor, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        indexes = [models.Index(fields=['slug'])]


class DiscountProduct(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(null=True, blank=True)
    param = RichTextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    oldprice = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField()
    discount_image = ProcessedImageField(upload_to='deals_images/%Y/%m', blank=True, max_length=250,
                                         processors=[ResizeToFit(None, 255)],
                                         format='JPEG',
                                         options={'quality': 70})

    category = TreeForeignKey('Category', related_name='products_discounts', on_delete=models.CASCADE)
    vendor = models.ForeignKey('Vendor', related_name='vendors_discounts', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return self.name

