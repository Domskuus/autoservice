from django.shortcuts import render
from django.http import HttpResponse
from .models import CarModel, Car, Order, OrderLine, Service

# Create your views here.

def index(request):
    num_car = CarModel.objects.all().count()
    num_orders = Order.objects.all().count()
    num_service = Service.objects.all().count()
    num_service_completed  = Order.objects.filter(status='Uzsakymas atliktas').count()

    context = {
        'num_car': num_car,
        'num_orders': num_orders,
        'num_service': num_service,
        'num_service_completed': num_service_completed
    }

    return render(request, 'index.html', context)