from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
        
admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)