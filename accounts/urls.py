from django.urls import path
from accounts.views import loginPage

urlpatterns = [
    path('login/', loginPage, name="login")
]