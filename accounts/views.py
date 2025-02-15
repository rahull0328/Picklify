from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.

def login_page(request):
    return render(request, 'accounts/login.html')

def register_page(request):
    if request.method == 'POST':
        
        #gathering form data after input
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        #validating form data to check if user exists or not
        user_obj = User.objects.filter(username = email)
        if user_obj.exists():
            messages.warning(request, 'Email already exists!')
            return HttpResponseRedirect(request.path_info)
        
        #creating a new user if not an existing user
        user_obj = User.objects.create(first_name = first_name, last_name = last_name, email = email, username = email, password = password)
        user_obj.set_password(password)  #hashing password before saving it
        user_obj.save()
        messages.success(request, "Mail Sent to Registered Email Address!")
        return HttpResponseRedirect(request.path_info)
        
    return render(request, 'accounts/register.html')