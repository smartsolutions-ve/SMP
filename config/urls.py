"""
URLs raíz del proyecto Smart Project Management.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda r: redirect('dashboard'), name='index'),
    path('auth/', include('apps.core.urls')),
    path('dashboard/', include('apps.core.urls_dashboard')),
    path('cotizaciones/', include('apps.cotizaciones.urls')),
    path('bd-costos/', include('apps.bd_costos.urls')),
    path('proyectos/', include('apps.proyectos.urls')),
    path('reportes/', include('apps.reportes.urls')),
    path('activos/', include('apps.activos.urls')),
    path('nomina/', include('apps.nomina.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
