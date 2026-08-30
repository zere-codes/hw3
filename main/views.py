from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from main.models import App, Category
def hw(request):
    return HttpResponse("This is my home work")

def index(request):
    apps = App.objects.order_by('-created_at').all()
    featured = App.objects.order_by('-price').first()
    categories = Category.objects.all()

    return render(request, 'main/index.html', {
        'apps': apps,
        'featured': featured,
        'categories': categories,
    })