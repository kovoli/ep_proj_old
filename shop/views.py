from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Product, Category


def home_page(request):
    return render(request, 'base.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    breadcrumbs = Category.get_ancestors(product.category)
    return render(request, 'shop/single_product.html', {'product': product,
                                                        'breadcrumbs': breadcrumbs})
