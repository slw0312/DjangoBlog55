from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request,'homeplate/index.html')

def about(request):
    return render(request,'homeplate/about.html')

def gallery(request):
    return render(request,'homeplate/gallery.html')

def contact(request):
    return render(request,'homeplate/contact.html')

def single_post(request):
    return render(request,'homeplate/single-post.html')