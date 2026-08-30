
# Register your models here.
from django.contrib import admin
from .models import Category, App, Review

admin.site.register(Category)
admin.site.register(App)
admin.site.register(Review)

