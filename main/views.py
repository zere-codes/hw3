from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def hw(request):
    return HttpResponse("This is my home work")