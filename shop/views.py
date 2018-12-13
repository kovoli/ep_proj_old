from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import CommentForm
from django.db.models import Min


def home_page(request):
    return render(request, 'base.html',)


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
                                                        'semilar_products': semilar_products})


def category_catalog(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # cat = Product.objects.filter(category__in=Category.objects.get(id=category.id).get_descendants())

    if category.get_level() <= 1:
        print(category.get_level())
        cat = category.get_descendants().order_by('tree_id', 'id', 'name')
        print(cat)
        return render(request, 'shop/category_catalog.html', {'category': category,
                                                          'cat': cat})
    if category.get_level() >= 2:
        products_list = Product.objects.filter(category__in=Category.objects.get(id=category.id)\
                                               .get_descendants(include_self=True)) \
                                               .annotate(min_price=Min('prices__price'))
        category = get_object_or_404(Category, slug=slug)
        cat = category.get_descendants(include_self=True).order_by('tree_id', 'id', 'name')

        print(category.is_leaf_node())
        print(category.get_family())
        return render(request, 'shop/category_product_list.html', {'products_list': products_list,
                                                                   'category': category,
                                                                   'cat': cat})

