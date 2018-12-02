from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Product, Category, Comment
from .forms import CommentForm


def home_page(request):
    return render(request, 'base.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    breadcrumbs = Category.get_ancestors(product.category)

    comments = product.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()

    else:
        comment_form = CommentForm()

    return render(request, 'shop/single_product.html', {'product': product,
                                                        'breadcrumbs': breadcrumbs,
                                                        'comments': comments,
                                                        'new_comment': new_comment,
                                                        'comment_form': comment_form})



def cat_list(request):
    cat = Product.objects.filter(category__in=Category.objects.get(id=30).get_descendants())
    print(cat)
