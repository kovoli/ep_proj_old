from django.contrib import admin
from .models import Product, Category, Price, Shop

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    readonly_fields = ['slug']


admin.site.register(Price)

@admin.register(Shop)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', ]
