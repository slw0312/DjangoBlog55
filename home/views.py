from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request,'homeplate/index.html')