from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category

def index(request):
    # Gets top five categories
    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
                    'categories': category_list}

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Sophie'}
    return render(request, 'rango/about.html', context=context_dict)