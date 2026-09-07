from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from main.models import App, Category, Review


def hw(request):
    return HttpResponse("This is my home work")


def index(request):
    apps=App.objects.all()
    return render(request, 'main/index.html', {'apps': apps})

def about(request):
    apps=App.objects.all()
    return render(request, 'main/about.html')

def reviews(request):
    reviews=Review.objects.all()
    return render(request, 'main/reviews.html', {'reviews': reviews})