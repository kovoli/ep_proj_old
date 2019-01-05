from django.shortcuts import render, get_object_or_404
from .models import DiscountProduct, Category
from shop.views import menu


def discount_product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    product_list = DiscountProduct.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        categories = category.get_descendants(include_self=True)
        product_list = product_list.filter(category=category)

    return render(request, 'discounts/discount_product_list.html', {'category': category,
                                                                    'categories': categories,
                                                                    'product_list': product_list
                                                                    })
