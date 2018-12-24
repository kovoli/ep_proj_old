from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Product, Category, Vendor
from .forms import CommentForm, BrandForms
from django.db.models import Min
from . import helpers
from .filters import BrandFilter

def menu(request):
    categories_home = Category.objects.all()
    return categories_home


def home_page(request):

    return render(request, 'base.html', {'menu': menu(request)})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    breadcrumbs = Category.get_ancestors(product.category)
    # Filter by Category > Exclude current Product > get the min price pro Product
    semilar_products = Product.objects.filter(category=product.category)\
        .exclude(id=product.id)\
        .annotate(min_price=Min('prices__price'))[:6]
    comments = product.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        print(comment_form)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()
            return redirect('shop:product_detail', slug=product.slug)

    else:
        comment_form = CommentForm()

    return render(request, 'shop/single_product.html', {'product': product,
                                                        'breadcrumbs': breadcrumbs,
                                                        'comments': comments,
                                                        'new_comment': new_comment,
                                                        'comment_form': comment_form,
                                                        'semilar_products': semilar_products,
                                                        'menu': menu(request)})


def category_catalog(request, slug=None):
    category = get_object_or_404(Category, slug=slug)
    breadcrumbs = Category.get_ancestors(category, include_self=True)
    # cat = Product.objects.filter(category__in=Category.objects.get(id=category.id).get_descendants())

    if category.get_level() <= 1:
        cat = category.get_descendants().order_by('tree_id', 'id', 'name')

        return render(request, 'shop/category_catalog.html', {'category': category,
                                                              'cat': cat,
                                                              'menu': menu(request),
                                                              'breadcrumbs': breadcrumbs})

    filter_brand = BrandForms(request.GET)
    print(BrandForms(request.GET))
    if category.get_level() >= 2:
        list_pro = Product.objects.filter(category__in=Category.objects.get(id=category.id)\
                                               .get_descendants(include_self=True)) \
                                               .annotate(min_price=Min('prices__price')).order_by('prices__price')


        vendors_ids = list_pro.values_list('vendor_id', flat=True).order_by().distinct()
        vendors = Vendor.objects.filter(id__in=vendors_ids)
        filter_brand.fields['brand'].queryset = Vendor.objects.filter(id__in=vendors_ids)

        products_list = helpers.pg_records(request, list_pro, 15)


        if filter_brand.is_valid():
            if filter_brand.cleaned_data['brand']:
                print('filter brand')

                list_pro = Product.objects.filter(category__in=Category.objects.get(id=category.id)\
                                                   .get_descendants(include_self=True)) \
                                                   .annotate(min_price=Min('prices__price'))\
                                                   .filter(vendor__in=filter_brand.cleaned_data['brand']).order_by('prices__price')
                products_list = helpers.pg_records(request, list_pro, 100)

        if filter_brand.is_valid():
            if filter_brand.cleaned_data['min_price']:
                print('filter min_price')
                list_pro = list_pro.filter(prices__price__gte=filter_brand.cleaned_data['min_price']).order_by('prices__price')
                products_list = helpers.pg_records(request, list_pro, 100)
        if filter_brand.is_valid():
            if filter_brand.cleaned_data['max_price']:
                print('filter max_price')
                list_pro = list_pro.filter(prices__price__lte=filter_brand.cleaned_data['max_price']).order_by('prices__price')
                products_list = helpers.pg_records(request, list_pro, 100)





        category = get_object_or_404(Category, slug=slug)
        cat = category.get_descendants(include_self=True).order_by('tree_id', 'id', 'name')
        last_node = category.get_siblings(include_self=True)







        return render(request, 'shop/category_product_list.html', {'products_list': products_list,
                                                                   'category': category,
                                                                   'vendors': vendors,
                                                                   'cat': cat,
                                                                   'last_node': last_node,
                                                                   'menu': menu(request),
                                                                   'breadcrumbs': breadcrumbs,
                                                                   'filter_brand': filter_brand,

                                                                   })


