from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<a href=/rango/about>about</a>")

def about(request):
    return HttpResponse("<a href=/rango/>index</a>")