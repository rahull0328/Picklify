from django.urls import path
from accounts.views import login_page, register_page, activate_email

urlpatterns = [
    path("register/", register_page, name="register"),
    path('login/', login_page, name="login"),
    path('activate/<email_token>/', activate_email, name="activate_email"),
]