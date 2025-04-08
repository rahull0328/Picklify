from django.urls import path
from products.views import get_product, view_categories, category_products

urlpatterns = [
   path('category/<slug:slug>/', category_products, name='category_products'),
   path('categories/', view_categories, name='view_categories'),
   path('<slug>/', get_product, name='get_product'),
]