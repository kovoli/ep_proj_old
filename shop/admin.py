from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Product, Category, Price, Shop, Vendor, Comment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'vendor',]
    readonly_fields = ['slug']
    list_filter = ('category', )
    search_fields = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'product', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'email', 'body')
    list_editable = ('active', )

@admin.register(Price)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['shop', 'name']
    readonly_fields = ['product']

@admin.register(Shop)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    readonly_fields = ('slug',)



@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['slug']
    search_fields = ['name']
