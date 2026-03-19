from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_view, name='activos_lista'),
    path('nuevo/', views.crear_view, name='activos_crear'),
    path('<uuid:activo_id>/', views.detalle_view, name='activos_detalle'),
    path('<uuid:activo_id>/editar/', views.editar_view, name='activos_editar'),
    path('api/buscar/', views.buscar_api, name='activos_buscar_api'),
]
