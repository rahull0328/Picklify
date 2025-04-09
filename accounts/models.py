from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.email import send_account_activation_email
from products.models import Product, ColorVariant, SizeVariant, Coupon

class Profile(BaseModel):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100 , null=True , blank=True)
    profile_image = models.ImageField(upload_to = 'profile')

    def get_cart_count(self):
        count = CartItems.objects.filter(cart__is_paid=False, cart__user=self.user).count()
        return count

class Cart(BaseModel):
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='carts')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def get_cart_total(self):
        total = 0
        for item in self.cart_items.all():
            total += item.get_total_price() 
        if self.coupon:
            if self.coupon.minimum_amount < total:
                return total - self.coupon.discount_price
        return total
    
class CartItems(BaseModel):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def get_product_price(self):
        price = [self.product.price]
        if self.color_variant:
            price.append(self.color_variant.price)
        if self.size_variant:
            price.append(self.size_variant.price)
        return sum(price)

    def get_total_price(self):
        return self.get_product_price() * self.quantity

    
@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance, email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)

class ContactMessage(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Remove unique=True for now
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)