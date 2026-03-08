from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_view, name='bd_costos_lista'),
    path('nuevo/', views.crear_item_view, name='bd_costos_crear'),
    path('<uuid:item_id>/editar/', views.editar_item_view, name='bd_costos_editar'),
    path('<uuid:item_id>/historial/', views.historial_item_view, name='bd_costos_historial'),
    path('<uuid:item_id>/toggle/', views.desactivar_item_view, name='bd_costos_toggle'),
    path('categorias/', views.categorias_view, name='bd_costos_categorias'),
    path('api/buscar/', views.buscar_items_api, name='bd_costos_buscar_api'),
]
