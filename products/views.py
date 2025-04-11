from django.shortcuts import render, get_object_or_404
from products.models import Product, Category
from django.http import HttpResponseNotFound

def get_random_products():
    return Product.objects.order_by('?')[:3]

def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        random_products = Product.objects.exclude(slug=slug).order_by('?')[:3]

        context = {
            'product': product,
            'random_products': random_products
        }

        size = request.GET.get('size')
        color = request.GET.get('color')

        if size:
            size = size.strip('"')
            context['selected_size'] = size

        if color:
            color = color.strip('"')
            context['selected_color'] = color

        if size or color:
            updated_price = product.get_price_based_on_variants(size=size, color=color)
            context['updated_price'] = updated_price

        return render(request, 'product/product.html', context)

    except Exception as e:
        print("Error:", e)
        return HttpResponseNotFound("An error occurred while fetching the product.")


def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'product/category.html', {'categories': categories})

def product_list_or_category(request, slug=None):
    categories = Category.objects.all()

    if slug:
        selected_category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=selected_category)
    else:
        selected_category = None
        products = Product.objects.all()

    return render(request, 'product/category.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    })