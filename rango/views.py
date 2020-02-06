from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request):
    # Gets top five categories and pages
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    visitor_cookie_handler(request)
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
                    'categories': category_list,
                    'pages': pages_list
                    }

    response = render(request, 'rango/index.html', context=context_dict)
    return response

def about(request):
    visitor_cookie_handler(request)
    context_dict = {'boldmessage': 'This tutorial has been put together by Sophie',
                    'visits': request.session['visits']}
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

@login_required
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

@login_required
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

def register(request):
    # Tracks success of registration
    registered = False

    # If post, process form data
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # Upon valid forms...
        if user_form.is_valid() and profile_form.is_valid():
            # Save form data to db
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            # Update user object
            user.save()

            # Set up profile
            # Commit false as user must be set 
            profile = profile_form.save(commit=False)
            profile.user = user

            # If picture is provided, put in UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            # Saving profile to db
            profile.save()

            # Registration success
            registered = True
        else:
            # Invalid form(s)
            print(user_form.errors, profile_form.errors)
    else:
        # Not HTTP POST
        # Render form using two blank ModelForm instances which take input
        user_form = UserForm()
        profile_form = UserProfileForm()
    # Template rendered depends on request
    return render(request,
                'rango/register.html',
                context = {'user_form': user_form,
                            'profile_form': profile_form,
                            'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        # Checks if account is active or not: logs in if true
        # Displays that their account has been disabled otherwise
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        # Invalid user
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")
    # If not POST, show form
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

# Helper function to retrieve cookie from request
def get_server_side_cookie(request, cookie, default_val=None):
    val =  request.session.get(cookie)
    if not val:
        val = default_val
    return val
 
# Helper function to get number of visits to site
def visitor_cookie_handler(request):
    # Gets the cookie's value if it exists
    # Defaults to 1 otherwise
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request,
                                                'last_visit',
                                                str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # If i thas been more than a day since last visit, increment visit cookie
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    # update/set visits cookie
    request.session['visits'] = visits