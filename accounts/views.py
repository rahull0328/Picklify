from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.

def loginPage(request):
    return render(request, 'accounts/login.html')

def registerPage(request):
    
    if request.method == 'POST':
        #fetching form data from UI
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        #checking whether user already exists
        userObj = User.objects.filter(username=username, email=email)
        if userObj.exists():
            messages.warning(request, 'Username or Email already exists !')
            return HttpResponseRedirect(request.path_info)
        
        #creating new user
        userObj = User.objects.create(username=username, email=email, password=password)
        userObj.set_password(password)
        userObj.save()
        messages.success(request, 'Mail has been sent to Registered Email Id !')
        
    return render(request, 'accounts/register.html')