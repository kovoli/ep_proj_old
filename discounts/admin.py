from django.contrib import admin
from .models import Category, DiscountProduct, Vendor
from mptt.admin import MPTTModelAdmin

@admin.register(DiscountProduct)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ['name']
    #readonly_fields = ['slug']
    #list_filter = ('category', )
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name']
    readonly_fields = ['slug']
    #list_filter = ('category', )
    search_fields = ['name']
    mptt_level_indent = 20

@admin.register(Vendor)
class VendoreAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['slug']
    #list_filter = ('category', )
    search_fields = ['name']