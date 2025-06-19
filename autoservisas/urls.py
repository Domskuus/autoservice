from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.carmodels, name='carmodels'),
    path('automobiliai/<int:carmodel_id>', views.carmodel, name='carmodel')
]