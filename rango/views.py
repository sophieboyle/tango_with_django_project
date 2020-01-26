from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index(request):
    # Gets top five categories and pages
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
                    'categories': category_list,
                    'pages': pages_list}

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Sophie'}
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        # Returns category if exists, otherwise, jumps to except
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form':form})

def add_page(request, category_name_slug):
    # Checks if the given category (via its slug) exists
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # Redirects to index if no category found
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug':
                                                category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html', context_dict)