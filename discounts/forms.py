from django import forms
from .models import Vendor


class BrandForms(forms.Form):
    brand = forms.ModelMultipleChoiceField(queryset=Vendor.objects.none(), widget=forms.CheckboxSelectMultiple(attrs={'onchange': "document.getElementById('branding').submit()"}), required=False)
    min_price = forms.IntegerField(label='от', required=False, widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control mb-2", "placeholder": "от:"
    }))
    max_price = forms.IntegerField(label='до', required=False, widget=forms.TextInput(attrs={
        'type': "text", 'class': "form-control mb-2", "placeholder": "до:"
    }))
    ordering = forms.ChoiceField(label="сортировка", required=False, choices=[
        ["-views", "по популярности"],
        ["prices__price", "дешевые сверху"],
        ["-prices__price", "дорогие сверху"]
    ], widget=forms.Select(attrs={'class': 'nice-select', 'onchange': "document.getElementById('ordering').submit()"}))
