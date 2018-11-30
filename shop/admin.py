from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Product, Category, Price, Shop, Vendor


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'vendor']
    readonly_fields = ['slug']


admin.site.register(Price)


@admin.register(Shop)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    readonly_fields = ('slug',)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['slug']
