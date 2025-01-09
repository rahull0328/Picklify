from django.urls import path
from accounts.views import loginPage, registerPage

urlpatterns = [
    path('login/', loginPage, name="login"),
    path('register/', registerPage, name="register")
]