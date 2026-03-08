"""
Middleware multi-tenant: identifica la empresa del usuario autenticado
y la adjunta al request como request.tenant.
"""
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


class TenantMiddleware:
    """
    Adjunta request.tenant (Empresa) basado en el usuario autenticado.
    Si el usuario está autenticado y no tiene empresa asignada, redirige al admin.
    """
    RUTAS_PUBLICAS = [
        '/auth/',
        '/admin/',
        '/static/',
        '/media/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tenant = None

        if request.user.is_authenticated:
            if hasattr(request.user, 'empresa') and request.user.empresa:
                request.tenant = request.user.empresa
            elif not self._es_ruta_publica(request.path):
                # Superusuario sin empresa: puede acceder al admin
                if request.user.is_superuser:
                    pass
                else:
                    return redirect('/admin/')

        response = self.get_response(request)
        return response

    def _es_ruta_publica(self, path):
        return any(path.startswith(r) for r in self.RUTAS_PUBLICAS)
