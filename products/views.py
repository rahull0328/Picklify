from django.shortcuts import render
from products.models import Product
from django.http import HttpResponseNotFound

# Create your views here.

def get_product(request, slug):
    try:
        product = Product.objects.get(slug =slug)
        return render(request, 'product/product.html', context = {'product': product})
    
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")  # Return a proper HTTP response
    
    except Exception as e:
        print(e)  # Log the error
        return HttpResponseNotFound("An error occurred while fetching the product.")