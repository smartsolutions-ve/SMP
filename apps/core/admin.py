from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Empresa, Usuario


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rif', 'telefono', 'email', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'moneda_default']
    search_fields = ['nombre', 'rif', 'email']


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'empresa', 'rol', 'email', 'is_active']
    list_filter = ['rol', 'empresa', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Smart PM', {'fields': ('empresa', 'rol', 'telefono', 'foto_perfil')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Smart PM', {'fields': ('empresa', 'rol', 'telefono')}),
    )
