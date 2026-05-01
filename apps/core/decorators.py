from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps

def tenant_required(view_func):
    """Decorador que verifica que el usuario logueado tiene una empresa asignada activa."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not getattr(request, 'tenant', None):
            messages.error(request, 'No tienes empresa asignada.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)

def permiso_costos_required(view_func):
    """Decorador adicional para módulos que requieren puede_ver_costos."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not getattr(request.user, 'puede_ver_costos', False):
            messages.error(request, 'No tienes permisos para ver costos o reportes.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
