from django.db.models import Count

from main.models import Category, App


def nav_categories(request):
    categories=list(
        Category.objects.annotate(apps_count=Count('app')).order_by('name')
    )

    featured=App.objects.order_by('-price')[:1]


    return {
        'categories': categories,
        'apps_total':App.objects.count(),
        'categories_total':len(categories),
        'featured':featured,
            }


def favorites_count(request):
    if request.user.is_authenticated:
        count = request.user.favorite_apps.count()
    else:
        count = 0

    return {'favorites_count': count}