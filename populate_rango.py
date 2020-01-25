import os

# Sets environmental variable for django to determine which settings to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
# Imports django project settings
django.setup()
# Performed following initialisation to avoid exception
from rango.models import Category, Page

def populate():
    # List of pages (as dicts) per category to add, each with a title and url.
    python_pages = [
        {'title':'Official Python Tutorial',
            'url':'http://docs.python.org/3/tutorial/',
            'views':40},
        {'title':'How to Think like a Computer Scientist',
            'url':'http://www.greenteapress.com/thinkpython/',
            'views':30},
        {'title':'Learn Python in 10 Minutes',
            'url':'http://www.korokithakis.net/tutorials/python/',
            'views':20},
    ]

    django_pages = [
        {'title':'Official Django Tutorial',
            'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
            'views':19},
        {'title':'Django Rocks',
            'url':'http://www.djangorocks.com/',
            'views':5},
        {'title':'How to Tango with Django',
            'url':'http://www.tangowithdjango.com/',
            'views':16}
    ]

    other_pages = [
        {'title':'Bottle',
            'url':'http://bottlepy.org/docs/dev/',
            'views':3},
        {'title':'Flask',
            'url':'http://flask.pocoo.org',
            'views':10}
    ]

    # Categories, each mapped to their respective list of pages
    cats = {'Python': {'pages': python_pages, 'views':128, 'likes':64},
            'Django': {'pages': django_pages, 'views':64, 'likes':32},
            'Other Frameworks': {'pages': other_pages, 'views':32, 'likes':16}}

    # For each category, adds the category and its respective pages
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    # Output added categories, and each of their pages to console
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    # Initialising page
    # Method indexed by 0 to get the page object
    # (excluding the bool as to whether it exists or not)
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    # Add page to db
    p.save()
    return p

def add_cat(name, views, likes):
    # Initialising category
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    # Add category to db
    c.save()
    return c

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()