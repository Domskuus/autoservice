from django.urls import path

from autoservice.urls import urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]