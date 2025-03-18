from django.urls import path
from products.views import get_product, get_category

urlpatterns = [
   path('<slug>/', get_product, name='get_product'),
   path('category/', get_category, name='get_category'),
]