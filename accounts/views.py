from django.shortcuts import render

# Create your views here.

def loginPage(request):
    return render(request, 'accounts/login.html')