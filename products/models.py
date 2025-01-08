from django.db import models
from base.models import BaseModel

# Create your models here.
class Category(BaseModel):
    catName = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    catImg = models.ImageField(upload_to="categories")
    
class Product(BaseModel):
    prodName = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    catId = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField()
    prodDesc = models.TextField()
    
class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    prodImg = models.ImageField(upload_to="products")