from django.urls import path, include
from . import views
from .views  import OrderListView

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.carmodels, name='carmodels'),
    path('automobiliai/<int:car_id>', views.carmodel, name='carmodel'),
    path('uzsakymai/',OrderListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:order_id>', views.order, name='uzsakymas'),
    path('vartotojai/', include('django.contrib.auth.urls'))
]