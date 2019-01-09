from django import forms
from .models import Vendor


class BrandForms(forms.Form):
    brand = forms.ModelMultipleChoiceField(queryset=Vendor.objects.none(),
                                           widget=forms.CheckboxSelectMultiple(
                                               attrs={'onchange': "document.getElementById('branding').submit()"}),
                                               required=False)
