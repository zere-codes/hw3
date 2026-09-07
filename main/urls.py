from django.contrib import admin
from django.urls import path, include, URLPattern
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('hw/', views.hw, name='hw'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('category/<int:category_id>/', views.category_detail, name='category'),
    path('app_detail/<int:app_id>/', views.app_detail, name='app_detail'),
    path('free/', views.free, name='free'),
]