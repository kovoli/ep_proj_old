from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('<slug:slug>/', views.product_detail)

]