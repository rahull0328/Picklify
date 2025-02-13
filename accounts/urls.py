from django.urls import path
from accounts.views import loginPage, registerPage, activateEmail

urlpatterns = [
    path('login/', loginPage, name="login"),
    path('register/', registerPage, name="register"),
    path('activate/<emailToken>', activateEmail, name="activatEmail")
]