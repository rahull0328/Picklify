from django.contrib import admin
from .models import Profile, Cart, CartItems

admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItems)