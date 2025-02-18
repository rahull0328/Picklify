from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from PIL import Image

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name

class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.IntegerField()
    product_description = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="product")

    def save(self, *args, **kwargs):
        """Resize the image to 60x60 before saving."""
        super(ProductImage, self).save(*args, **kwargs)

        # Get the image path
        img_path = self.image.path
        img = Image.open(img_path)

        # Resize image to 60x60
        img = img.resize((70, 70), Image.Resampling.LANCZOS)
        img.save(img_path)  # Save the resized image

    def __str__(self):
        return f"Image for {self.product.product_name}"