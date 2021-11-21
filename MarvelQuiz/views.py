from django.shortcuts import render
from django.http import HttpResponse, request

# Very first View (Boilerplate for now)

def temp(request):
    return HttpResponse("<h1>Hello World</h1>")

