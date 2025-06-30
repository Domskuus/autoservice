from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponse
from .models import CarModel, Car, Order, OrderLine, Service
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation
from .forms import OrderReviewForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required


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

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')

                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')

class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'uzsakymas.html'
    context_object_name = 'uzsakymas'
    form_class = OrderReviewForm

    def get_success_url(self):
        return reverse('uzsakymas', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        new_email = request.POST['email']
        if new_email == "":
            messages.error(request, f'El. paštas negali būti tuščias!')
            return redirect('profile')
        if request.user.email != new_email and User.objects.filter(email=new_email).exists():
            messages.error(request, f'Vartotojas su el. paštu {new_email} jau užregistruotas!')
            return redirect('profile')
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profile')

    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, "profile.html", context=context)