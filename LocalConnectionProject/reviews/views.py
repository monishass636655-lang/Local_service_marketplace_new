from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def review_list(request):
    return HttpResponse("List of reviews")

def add_review(request):
    return HttpResponse("Add a new review")