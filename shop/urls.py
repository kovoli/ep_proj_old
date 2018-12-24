from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('catalog/<slug:slug>/', views.category_catalog, name='category_catalog'),
    path('search/', views.search_products, name='search_products')
]