from django.shortcuts import render, get_object_or_404
from .models import DiscountProduct, Category, Vendor
from .forms import BrandForms
from shop.views import menu


def discount_product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    product_list = DiscountProduct.objects.all()
    context = {'category': category, 'categories': categories, 'product_list': product_list}

    if category_slug:
        filter_discount = BrandForms(request.GET)
        category = get_object_or_404(Category, slug=category_slug)
        categories = category.get_descendants(include_self=True)
        breadcrumbs = Category.get_ancestors(category, include_self=True)
        product_list = product_list.filter(category=category)

        vendors_ids = product_list.values_list('vendor_id', flat=True).order_by().distinct()
        vendors = Vendor.objects.filter(id__in=vendors_ids)
        print(vendors)
        filter_discount.fields['brand'].queryset = Vendor.objects.filter(id__in=vendors_ids)
        print(filter_discount['brand'])
        context = {'category': category, 'categories': categories,
                   'product_list': product_list, 'breadcrumbs': breadcrumbs,
                   'vendors': vendors, 'filter_discount': filter_discount}


    return render(request, 'discounts/discount_product_list.html', context)
