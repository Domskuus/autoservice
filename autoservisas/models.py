from django.db import models

# Create your models here.

class CarModel(models.Model):
    model = models.CharField(verbose_name="Modelis", max_length=200, help_text="Iveskite masinos modeli ")
    make = models.CharField(verbose_name="Gamintojas", max_length=200, help_text="Iveskite automobilio marke")

    def __str__(self):
        return f" Modelis {self.model}, marke  {self.make}"

class Car(models.Model):
    license_plate = models.CharField(verbose_name="Valstybinis Numeris", max_length=7, help_text="Iveskite valstybini numeri")
    auto_model = models.CharField(verbose_name="Modelis", max_length=200, help_text="Iveskite masinos modeli ")
    vin_number = models.CharField(verbose_name="VIN Kodas", max_length=20, help_text="Iveskite VIN koda")
    client_name = models.CharField(verbose_name="Klientas", max_length=20)
    car_model = models.ForeignKey(to="CarModel", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f" Masinos modelis {self.car_model}, masinos numeris {self.license_plate}"

class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=100)
    price = models.DecimalField(verbose_name="Kaina")

    def __str__(self):
        return f" Serviso pavadinimas {self.name}, kaina  {self.price}"

