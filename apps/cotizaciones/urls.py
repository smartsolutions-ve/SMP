from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_view, name='cotizaciones_lista'),
    path('nueva/', views.crear_view, name='cotizacion_crear'),
    path('<uuid:cot_id>/', views.detalle_view, name='cotizacion_detalle'),
    path('<uuid:cot_id>/editar/', views.editar_view, name='cotizacion_editar'),
    path('<uuid:cot_id>/estado/', views.cambiar_estado_view, name='cotizacion_estado'),
    path('<uuid:cot_id>/convertir/', views.convertir_proyecto_view, name='cotizacion_convertir'),
    path('<uuid:cot_id>/duplicar/', views.duplicar_view, name='cotizacion_duplicar'),
    path('<uuid:cot_id>/pdf/', views.pdf_view, name='cotizacion_pdf'),
]
