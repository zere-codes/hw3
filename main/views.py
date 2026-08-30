from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from main.models import App, Category
def hw(request):
    return HttpResponse("This is my home work")

def index(request):
    app = App.objects.first()
    return HttpResponse(f"Приложение дня: {app.name}")