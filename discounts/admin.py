from django.contrib import admin
from .models import Category, DiscountProduct, Vendor


@admin.register(DiscountProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    #readonly_fields = ['slug']
    #list_filter = ('category', )
    search_fields = ['name']
