from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# Create your views here.
from main.models import App, Category, Review


def hw(request):
    return HttpResponse("This is my home work")

def index(request):
    apps = App.objects.all()
    categories = Category.objects.all()

    return render(request, 'main/index.html', {
        'apps': apps,
        'categories': categories,
    })

def about(request):
    apps=App.objects.all()
    return render(request, 'main/about.html')

def reviews(request):
    reviews=Review.objects.all()
    return render(request, 'main/reviews.html', {'reviews': reviews})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    apps = App.objects.filter(category=category)
    return render(request, 'main/category_detail.html', {
        'categories': category,
        'apps': apps,
    })

def app_detail(request, app_id):
    app = get_object_or_404(App, id=app_id)

    return render(request, 'main/app_detail.html', {
        'app': app,

    })

def free(request):
    apps=App.objects.filter(price=0)
    return render(request, 'main/free.html' , {'apps': apps})