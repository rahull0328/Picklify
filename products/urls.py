from django.urls import path
from products.views import get_product, product_list_or_category

urlpatterns = [
    # View all products or filtered by category
    path('', product_list_or_category, name='product_list'),
    path('products/category/<slug:slug>/', product_list_or_category, name='category_products'),

    # Product detail page
    path('<slug>/', get_product, name='get_product'),
]
