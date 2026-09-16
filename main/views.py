from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# Create your views here.
from main.models import App, Category, Review
from django.db.models import Q
from django.core.paginator import Paginator

def hw(request):
    return HttpResponse("This is my home work")

def index(request):
    apps = App.objects.all()
    categories = Category.objects.all()
    q = request.GET.get('q', '')


    if q:
        apps = App.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))

    else:
        apps = App.objects.order_by('-created_at')


    return render(request, 'main/index.html', {
        'apps': apps,
        'categories': categories,
        'q': q,
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
    q = request.GET.get('q', '')

    if q:
        apps = App.objects.filter(Q(name__icontains=q) | Q(description__icontains=q), category=category)

    else:
        apps = App.objects.order_by('-created_at').filter(category=category)

    paginator = Paginator(apps, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'main/category_detail.html', {
        'category': category,
        'apps': apps,
        'page_obj': page_obj,
        'q': q,
    })

def app_detail(request, app_id):
    app = get_object_or_404(App, id=app_id)

    return render(request, 'main/app_detail.html', {
        'app': app,

    })





def free(request):
    apps=App.objects.filter(price=0)
    return render(request, 'main/free.html' , {'apps': apps})

def new(request):
    apps = App.objects.order_by('-created_at')[:5]
    paginator = Paginator(apps, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)




    return render(request, 'main/new.html', {
        'apps': apps,
        'page_obj': page_obj,

    })
