from django.contrib import admin
from .models import Profile, Cart, CartItems, ContactMessage, BillingDetails

admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(ContactMessage)
admin.site.register(BillingDetails)