from django.db import models

# Create your models here.

class CarModel(models.Model):
    model = models.CharField(verbose_name="Modelis", max_length=200, help_text="Iveskite masinos modeli ")
    make = models.CharField(verbose_name="Gamintojas", max_length=200, help_text="Iveskite automobilio marke")

    def __str__(self):
        return f" {self.make}, {self.model}"

    class Meta:
        verbose_name = "Automobilio Modelis"
        verbose_name_plural = "Automobilių Modeliai"



class Car(models.Model):
    license_plate = models.CharField(verbose_name="Valstybinis Numeris", max_length=7, help_text="Iveskite valstybini numeri")
    auto_model = models.ForeignKey(to="CarModel", on_delete=models.SET_NULL, null=True, blank=True)
    vin_number = models.CharField(verbose_name="VIN Kodas", max_length=20, help_text="Iveskite VIN koda")
    client_name = models.CharField(verbose_name="Klientas", max_length=20)

    def __str__(self):
        return f" Masinos modelis {self.auto_model}, masinos numeris {self.license_plate}"

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=100)
    price = models.IntegerField(verbose_name="Kaina")

    def __str__(self):
        return f"{self.name},{self.price}"

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class Order(models.Model):
    car = models.ForeignKey(to="Car", verbose_name="Automobilis", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    # TODO total

    def __str__(self):
        return f" Uzsakymas {self.id}, Data : {self.date}, Automobilis  {self.car}"

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"



class OrderLine(models.Model):
    order = models.ForeignKey(to="Order",verbose_name="Uzsakymas", on_delete=models.CASCADE)
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(verbose_name="Kiekis")

    def total_sum(self):
        if self.service:
            return self.quantity * self.service.price
        return 0

    def __str__(self):
        return f"{self.service} - {self.quantity}, Bendra Suma :{self.total_sum()}"

    class Meta:
        verbose_name = "Užsakymo eilutė"
        verbose_name_plural = "Užsakymo eilutės"