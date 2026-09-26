from django.contrib import admin
from django.urls import path, include, URLPattern
from . import views



app_name = 'main'

urlpatterns=[
    path('', views.AppListView.as_view(), name='index'),
    path('hw/', views.hw, name='hw'),
    path('about/',views.AboutView.as_view(), name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('category/<int:category_id>/', views.category_detail, name='category'),
    path('app_detail/<int:app_id>/<str:app_name>/', views.AppDetailView.as_view(), name='app_detail'),
    path('free/', views.free, name='free'),
    path('new/', views.new, name='new'),
    path('api/review_detail/<int:review_id>/', views.review_detail, name='review_detail'),
    path('cheap/', views.cheap_apps, {'max_price':500}, name='cheap_apps'),
    path('premium/', views.cheap_apps, {'min_price': 5000}, name='premium_apps'),
    path('add_review/<int:app_id>', views.add_review, name='add_review'),
]

