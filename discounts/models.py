from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
# Удаление фотографии после удаления скидки
import os
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class DiscountProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    param = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    oldprice = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField()
    discount_image = ProcessedImageField(upload_to='deals_images/%Y/%m', blank=True, max_length=250,
                                      processors=[ResizeToFit(None, 255)],
                                      format='JPEG',
                                      options={'quality': 70})

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return self.name

