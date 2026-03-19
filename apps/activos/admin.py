from django.contrib import admin
from .models import ActivoCliente


@admin.register(ActivoCliente)
class ActivoClienteAdmin(admin.ModelAdmin):
    list_display = ['codigo_equipo', 'nombre', 'tipo', 'cliente_nombre', 'estado', 'activo']
    list_filter = ['tipo', 'estado', 'activo']
    search_fields = ['codigo_equipo', 'nombre', 'cliente_nombre', 'serial']
