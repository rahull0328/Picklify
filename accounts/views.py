from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .models import Profile
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from accounts.models import Cart, CartItems, SizeVariant, ColorVariant, ContactMessage
from products.models import *
import logging

logger = logging.getLogger(__name__)

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        #returning the user error if account doesn't exist
        if not user_obj.exists():
            messages.warning(request, 'Account not found!')
            return HttpResponseRedirect(request.path_info)

        #returning the user error if email isn't verified
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified!')
            return HttpResponseRedirect(request.path_info)

        #authenticating the user and redirecting to home page if user is valid and email is verified
        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        messages.warning(request, 'Invalid Creds!')
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/login.html')

def register_page(request):
    if request.method == 'POST':
        
        #gathering form data after input
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        #validating form data to check if user exists or not
        user_obj = User.objects.filter(username = email)
        if user_obj.exists():
            messages.warning(request, 'Email already exists!')
            return HttpResponseRedirect(request.path_info)
        
        #creating a new user if not an existing user
        user_obj = User.objects.create(first_name = first_name, last_name = last_name, email = email, username = email, password = password)
        user_obj.set_password(password)  #hashing password before saving it
        user_obj.save()
        messages.success(request, "Mail Sent to Registered Email Address!")
        return HttpResponseRedirect(request.path_info)
        
    return render(request, 'accounts/register.html')

def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    
    except Exception as e:
        return HttpResponse('Invalid Email Token !')    
    
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

def cart(request):
    cart = None
    cart_items = []

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_paid=False).first()

        if cart:
            cart_items = CartItems.objects.filter(cart=cart)
        else:
            messages.warning(request, "Your cart is empty.")
    else:
        messages.warning(request, "Please log in to view your cart.")

    # Handle coupon only if user is logged in and cart exists
    if request.method == 'POST':
        if not request.user.is_authenticated or not cart:
            messages.warning(request, "You must be logged in to apply a coupon.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        coupon_code = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__iexact=coupon_code).first()

        if not coupon_obj:
            messages.warning(request, 'Invalid Coupon Code!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart.coupon:
            messages.warning(request, 'A coupon is already applied to your cart.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj.is_expired:
            messages.warning(request, "Coupon is Expired!.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart.get_cart_total() < coupon_obj.minimum_amount:
            messages.warning(request, f'Cart Value Should Be Greater than {coupon_obj.minimum_amount}!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Apply the coupon
        cart.coupon = coupon_obj
        cart.save()
        messages.success(request, 'Coupon Applied Successfully!')

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'coupon': cart.coupon if cart else None
    }

    return render(request, 'cart/cart.html', context)


def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid=cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request, 'Coupon Removed Successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def add_to_cart(request, uid):
    user = request.user

    if not user.is_authenticated:
        return redirect('accounts/login.html')  # Redirect to login page

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
    cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def remove_from_cart(request, cart_item_uid):
    user = request.user

    if not user.is_authenticated:
        return redirect('accounts/login.html')  # Redirect to login page
    
    try:
        cart_item = CartItems.objects.get(uid =cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(f"Error removing from cart: {e}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Create a new contact message object
        try:
            contact_obj = ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
            contact_obj.save()
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            logger.error(f"Error saving contact message: {e}")  # Logs the actual error
            messages.warning(request, f"Error: {e}")  # Show exact error (only for debugging)
            return HttpResponseRedirect(request.path_info)

        return HttpResponseRedirect(request.path_info)

    return render(request, 'contact/contact.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/')
