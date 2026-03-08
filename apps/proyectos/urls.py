from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_view, name='proyectos_lista'),
    path('<uuid:proyecto_id>/', views.detalle_view, name='proyecto_detalle'),
    path('<uuid:proyecto_id>/estado/', views.cambiar_estado_view, name='proyecto_estado'),
    path('<uuid:proyecto_id>/partida/<uuid:partida_id>/avance/', views.registrar_avance_view, name='proyecto_avance'),
    path('<uuid:proyecto_id>/fotos/', views.subir_fotos_view, name='proyecto_fotos'),
    path('<uuid:proyecto_id>/orden-cambio/', views.orden_cambio_view, name='proyecto_oc_crear'),
    path('<uuid:proyecto_id>/orden-cambio/<uuid:oc_id>/aprobar/', views.aprobar_orden_cambio_view, name='proyecto_oc_aprobar'),
]
