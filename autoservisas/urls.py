from django.urls import path, include
from . import views
from .views  import OrderListView, OrderDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.carmodels, name='carmodels'),
    path('automobiliai/<int:car_id>', views.carmodel, name='carmodel'),
    path('uzsakymai/',OrderListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:order_id>', views.order, name='uzsakymas'),
    path('vartotojai/', include('django.contrib.auth.urls')),
    path('search/', views.search, name='search'),
    path('mano_uzsakymai', views.MyOrderInstanceListView.as_view(), name="mano_uzsakymai"),
    path('register/', views.register, name='register'),
]