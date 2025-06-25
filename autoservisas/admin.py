from django.contrib import admin
from .models import CarModel, Service, Car, Order, OrderLine
 # Register your models here.

class carAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'auto_model', 'license_plate', 'vin_number' ]
    list_filter = ['client_name', "auto_model"]
    search_fields = ['license_plate', 'vin_number']

class OrderInstanceLine(admin.TabularInline):
    model = OrderLine
    can_delete = True
    extra = 1



class OrderAdmin(admin.ModelAdmin):
    list_display =  ['car', 'date', 'status', 'client', 'due_back']
    inlines = [OrderInstanceLine]
    list_filter = ['status', 'due_back']
    list_editable = ['status', 'due_back']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'quantity', 'service', 'bendra_suma']

    def bendra_suma(self, obj):
        return obj.total_sum()
    bendra_suma.short_description = 'Bendra Suma'








admin.site.register(CarModel)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, carAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)