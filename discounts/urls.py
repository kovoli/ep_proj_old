from django.urls import path
from . import views

app_name = 'discounts'

urlpatterns = [
    path('poducts/', views.discount_product_list, name='discount_list'),
    path('poducts/<slug:category_slug>/', views.discount_product_list, name='discount_category_catalog')
]
