from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import CarModel, Car, Order, OrderLine, Service
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

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
    order = get_object_or_404(Order, pk=order_id)
    orderlines = OrderLine.objects.filter(order=order)
    total_price = sum(line.total_sum() for line in orderlines)
    return render(request, 'uzsakymas.html', {'uzsakymas' : order,'orderlines': orderlines, 'total_price': total_price})

def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')

    car_search_results = Car.objects.filter(
        Q(license_plate__icontains=query) | Q(auto_model__model__icontains=query) | Q(vin_number__icontains=query) | Q(
            client_name__icontains=query) | Q(auto_model__make__icontains=query))

    order_search_results = OrderLine.objects.filter(
        Q(order__status__icontains=query) | Q(service__name__icontains=query))

    context = {
        "query": query,
        "cars": car_search_results,
        "orders": order_search_results

    }
    return render(request, template_name="search.html", context=context)

class MyOrderInstanceListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'mano_uzsakymai.html'
    context_object_name = 'mano_uzsakymai'

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)
