from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def booking_home(request):
    return HttpResponse("Bookings app working")