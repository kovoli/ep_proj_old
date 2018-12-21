from .models import Vendor
import django_filters


def brands(request):
    if request is None:
        return Vendor.objects.none()


class BrandFilter(django_filters.FilterSet):
    def my_filter(self, queryset):
        return queryset
    brand = django_filters.ModelChoiceFilter(method='my_filter', queryset=my_filter)


