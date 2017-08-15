from django.http import HttpResponse

from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello world!")

def classify(request):
    context = {}
    return render(request, "index.html", context)