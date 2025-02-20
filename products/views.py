from django.shortcuts import render
from products.models import Product
from django.http import HttpResponseNotFound

def get_random_products():
    """Returns 3 random products"""
    return Product.objects.order_by('?')[:3]

def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        random_products = Product.objects.exclude(slug=slug).order_by('?')[:3]
        return render(request, 'product/product.html', 
                     context={'product': product, 'random_products': random_products})
    
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")
    
    except Exception as e:
        print(e)
        return HttpResponseNotFound("An error occurred while fetching the product.")
