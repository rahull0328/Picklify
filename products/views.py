from django.shortcuts import render, redirect
from products.models import Product
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from accounts.models import Cart, CartItems, SizeVariant, ColorVariant

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

@login_required  # Ensures only logged-in users can access this function
def add_to_cart(request, uid):
    user = request.user

    if not user.is_authenticated:  # Double-check for extra security
        return redirect('login')  # Redirect to login page

    try:
        product = Product.objects.get(uid=uid)
    except Product.DoesNotExist:
        return HttpResponseBadRequest("Invalid product ID")  # Handle bad product ID

    # Get or create cart for the logged-in user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    # Handle size variant if applicable
    variant = request.GET.get('variant')
    size_variant = None
    if variant:
        try:
            size_variant = SizeVariant.objects.get(size_name=variant)
        except SizeVariant.DoesNotExist:
            return HttpResponseBadRequest("Invalid size variant")

    # Handle color variant if applicable
    color = request.GET.get('color')
    color_variant = None
    if color:
        try:
            color_variant = ColorVariant.objects.get(color_name=color)
        except ColorVariant.DoesNotExist:
            return HttpResponseBadRequest("Invalid color variant")

    # Create cart item with size and color variants
    cart_item = CartItems.objects.create(cart=cart, product=product, size_variant=size_variant, color_variant=color_variant)
    cart_item.save()  # Ensure it's saved with all attributes

    print(f"Added to Cart - Product: {product.uid}, Size: {variant}, Color: {color}")  # Debugging

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))