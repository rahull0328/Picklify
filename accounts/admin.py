from django.contrib import admin
from .models import Profile, Cart, CartItems, ContactMessage

admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(ContactMessage)