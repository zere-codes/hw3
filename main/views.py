from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect
# Create your views here.
from main.models import App, Category, Review
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, DetailView




@require_GET
def hw(request):
    return HttpResponse("This is my homework")
class AppListView(ListView):
    model = App
    template_name = 'main/index.html'
    paginate_by =4
    context_object_name = 'apps'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        sort=self.request.GET.get('sort', 'new')

        if q:
            apps = App.objects.filter(Q(name__icontains=q) | Q(description__icontains=q)).order_by('name')

        else:
            apps = App.objects.order_by('-created_at')

        return apps

class AboutView(TemplateView):
    template_name = 'main/about.html'


class AppDetailView(DetailView):
    model = App
    template_name = 'main/app_detail.html'
    context_object_name = 'app'
    pk_url_kwarg = 'app_id'

    def get_object(self):
        app=super().get_object()
        if app.name!=self.kwargs['app_name']:
            return redirect('main:app_detail', app.id, app.name)
        return app

def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    data={
        'review_id': review.id,
        'app': review.app.name,
        'username': review.username,
        'comment': review.comment,
        'stars': review.stars,
        'recommended': review.recommended,
        'created_at': review.created_at,
    }

    return JsonResponse(data)






def reviews(request):
    reviews=Review.objects.all()
    return render(request, 'main/reviews.html', {'reviews': reviews})

def category_detail(request, category_id):
    categories = Category.objects.all()
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
        'categories': categories,
        'apps': apps,
        'page_obj': page_obj,
        'q': q,
    })
#
# def app_detail(request, app_id, app_name):
#     app = get_object_or_404(App, id=app_id)
#
#     if app_name != app.name:
#         return redirect('main:app_detail', app.id, app.name)
#
#
#     print(app_name)
#
#     return render(request, 'main/app_detail.html', {
#         'app': app,
#
#     })







def free(request):
    apps=App.objects.filter(price=0)
    return render(request, 'main/free.html' , {'apps': apps})

def new(request):
    apps = App.objects.order_by('-created_at')
    paginator = Paginator(apps, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)




    return render(request, 'main/new.html', {
        'page_obj': page_obj,

    })

def cheap(request):
    apps = App.objects.filter(price__lte=500)
    paginator = Paginator(apps, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/cheap.html', {'page_obj': page_obj})

def cheap_apps(request, min_price=None, max_price=None):
    if min_price is not None:
        apps = App.objects.filter(price__gte=500)
    elif max_price is not None:
        apps = App.objects.filter(price__lte=5000)

    paginator = Paginator(apps, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'main/cheap.html', {'page_obj': page_obj})

