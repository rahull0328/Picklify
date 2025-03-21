from django.shortcuts import render, redirect
from products.models import Product
from django.http import HttpResponseNotFound

def get_random_products():
    return Product.objects.order_by('?')[:3]

def get_product(request, slug):
    
    try:
        product = Product.objects.get(slug=slug)
        random_products = Product.objects.exclude(slug=slug).order_by('?')[:3]
        
        context = {'product': product, 'random_products': random_products}

        # Handle size selection and update price
        if request.GET.get('size'):
            size = request.GET.get('size').strip('"')
            price = product.get_product_size_by_size(size)  # Ensure this method exists in your model
            context['selected_size'] = size
            context['updated_price'] = price

        # Handle color selection and filter products by color
        if request.GET.get('color'):
            selected_color = request.GET.get('color').strip('"')
            similar_products = Product.objects.filter(color_variant__color_name=selected_color)
            context['selected_color'] = selected_color
            context['similar_products'] = similar_products  # List of products with the selected color

        return render(request, 'product/product.html', context)

    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found")
    
    except Exception as e:
        print(e)
        return HttpResponseNotFound("An error occurred while fetching the product.")

def get_category(request):
    return render(request, 'product/category.html')
        