from django.shortcuts import render
from django.http import HttpResponse
from .models import CarModel, Car, Order, OrderLine, Service
from django.views import generic
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    num_car = CarModel.objects.all().count()
    num_orders = Order.objects.all().count()
    num_service = Service.objects.all().count()
    num_service_completed  = Order.objects.filter(status='Uzsakymas atliktas').count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_car': num_car,
        'num_orders': num_orders,
        'num_service': num_service,
        'num_service_completed': num_service_completed,
        'num_visits' : num_visits
    }

    return render(request, 'index.html', context)




def carmodels(request):

    cars = Car.objects.select_related('auto_model').all()
    paginator = Paginator(cars, per_page=2)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {'cars': paged_cars}
    return render(request, 'automobiliai.html', {'cars': cars})

def carmodel(request, car_id):
    carmodel = Car.objects.get(pk=car_id)
    return render(request, 'automobilis.html', {'automobilis' : carmodel})

class OrderListView(generic.ListView):
    model = Order
    template_name = 'uzsakymai.html'
    context_object_name = 'uzsakymai'
    paginate_by = 3

def order(request, order_id):
    order = OrderLine.objects.get(pk=order_id)
    total_price = order.quantity * order.service.price
    return render(request, 'uzsakymas.html', {'uzsakymas' : order, 'total_price': total_price})

# class CarListView(generic.ListView):
#     model = Car
#     template_name = 'automobiliai.html'
#     context_object_name = 'automobiliai'
#     paginate_by = 3



# class OderListView(generic.Listview):
#     model = Order
#     template_name = 'orders.html'
#     context_object_name = 'orders'
