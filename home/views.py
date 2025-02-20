from django.shortcuts import render
from products.views import get_random_products

def index(request):
    context = {'products': get_random_products()}
    return render(request, 'home/index.html', context)
