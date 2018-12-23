if filter_brand.is_valid():
    if filter_brand.cleaned_data:
        print(filter_brand.cleaned_data)

        list_pro = Product.objects.filter(category__in=Category.objects.get(id=category.id) \
                                          .get_descendants(include_self=True)) \
            .annotate(min_price=Min('prices__price')) \
            .filter(vendor__in=filter_brand.cleaned_data['brand'])
        products_list = helpers.pg_records(request, list_pro, 12)

if filter_brand.is_valid():
    print(request.GET)
    if 'min_price' in request.GET:
        print('ok')
    if filter_brand.cleaned_data['min_price']:
        list_pro = list_pro.filter(prices__price__gte=filter_brand.cleaned_data['min_price'])
        products_list = helpers.pg_records(request, list_pro, 12)