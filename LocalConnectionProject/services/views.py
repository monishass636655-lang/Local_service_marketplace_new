from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def service_list(request):
    return HttpResponse("Welcome to Local Service Marketplace")
from django.shortcuts import render
from .models import Service

def service_list(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

from django.shortcuts import render, get_object_or_404
from .models import Service

def service_list(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

def service_detail(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'service_detail.html', {'service': service})