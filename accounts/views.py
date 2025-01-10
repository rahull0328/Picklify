from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Profile

# Create your views here.

def loginPage(request):
    
    if request.method == 'POST':
        #fetching form data from UI
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        #checking whether user already exists
        userObj = User.objects.filter(email=email)
        if not userObj.exists():
            messages.error(request, 'Account Not Found !')
            return HttpResponseRedirect(request.path_info)
        
        #checking whether email is verified or not before logging in
        if not userObj[0].profile.isEmailVerified:
            messages.warning(request, 'Email is not verified yet !')
            return HttpResponseRedirect(request.path_info)
        
        #logging the user in
        userObj = authenticate(email=email, password=password)
        #if successfull login then this block will be executed
        if userObj:
            login(request, userObj)
            return redirect('/')
        
        #else error
        messages.error(request, 'Invalid Email Or Password !')
        return HttpResponseRedirect(request.path_info)
            
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
        messages.success(request, 'Mail has been sent to Registered Email !')
        
    return render(request, 'accounts/register.html')