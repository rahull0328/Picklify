from django.urls import path
from cart.views import cart_page

urlpatterns = [
    path("", cart_page, name="cart"),
]