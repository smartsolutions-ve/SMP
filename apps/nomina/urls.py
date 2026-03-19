from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cargos_view, name='nomina_lista'),
    path('nuevo/', views.crear_cargo_view, name='nomina_crear'),
    path('<uuid:cargo_id>/', views.detalle_cargo_view, name='nomina_detalle'),
    path('<uuid:cargo_id>/editar/', views.editar_cargo_view, name='nomina_editar'),
    path('hh/<uuid:partida_id>/', views.registrar_hh_view, name='nomina_registrar_hh'),
    path('api/buscar/', views.buscar_cargos_api, name='nomina_buscar_api'),
]
