from django.shortcuts import render, get_object_or_404
from .models import DiscountProduct, Category, Vendor
from .forms import BrandForms
from shop import helpers
from shop.views import menu


def discount_product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    list_pro = DiscountProduct.objects.all()
    product_list = helpers.pg_records(request, list_pro, 6)
    context = {'category': category, 'categories': categories, 'product_list': product_list, 'menu': menu(request)}

    if category_slug:
        filter_discount = BrandForms(request.GET)
        category = get_object_or_404(Category, slug=category_slug)
        categories = category.get_descendants(include_self=True)
        breadcrumbs = Category.get_ancestors(category, include_self=True)

        list_pro = DiscountProduct.objects.filter(category__in=Category.objects.get(id=category.id)\
                                                                .get_descendants(include_self=True))

        vendors_ids = list_pro.values_list('vendor_id', flat=True).order_by().distinct()
        vendors = Vendor.objects.filter(id__in=vendors_ids)
        filter_discount.fields['brand'].queryset = Vendor.objects.filter(id__in=vendors_ids)

        product_list = helpers.pg_records(request, list_pro, 6)
        context = {'category': category, 'categories': categories,
                   'product_list': product_list, 'breadcrumbs': breadcrumbs,
                   'vendors': vendors, 'filter_discount': filter_discount,
                   'menu': menu(request)}

        if filter_discount.is_valid():
            if filter_discount.cleaned_data['brand']:
                list_pro = DiscountProduct.objects.filter(category__in=Category.objects.get(id=category.id)\
                                                                                       .get_descendants(include_self=True))\
                                                                                       .filter(vendor__in=filter_discount.cleaned_data['brand'])
                product_list = helpers.pg_records(request, list_pro, 100)
                context = {'category': category, 'categories': categories,
                           'product_list': product_list, 'breadcrumbs': breadcrumbs,
                           'vendors': vendors, 'filter_discount': filter_discount,
                           'menu': menu(request)}


    return render(request, 'discounts/discount_product_list.html', context)
