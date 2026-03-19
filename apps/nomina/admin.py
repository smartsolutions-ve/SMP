from django.contrib import admin
from .models import CargoTrabajador, HistorialCostoHH, RegistroHH


@admin.register(CargoTrabajador)
class CargoTrabajadorAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'nivel', 'costo_hora', 'activo']
    list_filter = ['nivel', 'activo']
    search_fields = ['codigo', 'nombre']


@admin.register(RegistroHH)
class RegistroHHAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'cargo', 'horas', 'cantidad_trabajadores', 'costo_total']
    list_filter = ['fecha', 'cargo']
