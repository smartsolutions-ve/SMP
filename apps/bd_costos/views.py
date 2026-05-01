"""
Vistas del módulo Base de Datos de Costos.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from decimal import Decimal, InvalidOperation
import json

from .models import ItemCosto, CategoriaItem, HistorialPrecio
from apps.core.models import Usuario


from apps.core.decorators import tenant_required


@tenant_required
def lista_view(request):
    empresa = request.tenant
    items = ItemCosto.objects.filter(empresa=empresa)

    # Filtros
    busqueda = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '')
    categoria_id = request.GET.get('categoria', '')
    activo = request.GET.get('activo', 'true')

    if busqueda:
        items = items.filter(
            Q(codigo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(especificaciones__icontains=busqueda)
        )
    if tipo:
        items = items.filter(tipo=tipo)
    if categoria_id:
        items = items.filter(categoria_id=categoria_id)
    if activo != 'todos':
        items = items.filter(activo=(activo == 'true'))

    items = items.select_related('categoria').order_by('tipo', 'codigo')

    categorias = CategoriaItem.objects.filter(empresa=empresa, activo=True).order_by('codigo')

    context = {
        'items': items,
        'categorias': categorias,
        'tipos': ItemCosto.TIPOS,
        'busqueda': busqueda,
        'tipo_sel': tipo,
        'categoria_sel': categoria_id,
        'activo_sel': activo,
        'total_items': items.count(),
    }
    return render(request, 'bd_costos/lista.html', context)


@tenant_required
def crear_item_view(request):
    empresa = request.tenant
    categorias = CategoriaItem.objects.filter(empresa=empresa, activo=True).order_by('codigo')

    if request.method == 'POST':
        try:
            codigo = request.POST.get('codigo', '').strip().upper()
            descripcion = request.POST.get('descripcion', '').strip()
            tipo = request.POST.get('tipo', '')
            unidad = request.POST.get('unidad', 'un')
            unidad_custom = request.POST.get('unidad_custom', '').strip()
            precio_str = request.POST.get('precio_actual', '0').replace(',', '.')
            moneda = request.POST.get('moneda', 'USD')
            categoria_id = request.POST.get('categoria') or None
            especificaciones = request.POST.get('especificaciones', '').strip()
            proveedor = request.POST.get('proveedor_preferido', '').strip()
            notas = request.POST.get('notas', '').strip()

            # Validaciones
            if not codigo:
                messages.error(request, 'El código es requerido.')
                raise ValueError()
            if not descripcion:
                messages.error(request, 'La descripción es requerida.')
                raise ValueError()
            if ItemCosto.objects.filter(empresa=empresa, codigo=codigo).exists():
                messages.error(request, f'Ya existe un ítem con el código "{codigo}".')
                raise ValueError()

            precio = Decimal(precio_str)
            if precio <= 0:
                messages.error(request, 'El precio debe ser mayor que 0.')
                raise ValueError()

            item = ItemCosto.objects.create(
                empresa=empresa,
                codigo=codigo,
                descripcion=descripcion,
                tipo=tipo,
                unidad=unidad,
                unidad_custom=unidad_custom,
                precio_actual=precio,
                moneda=moneda,
                categoria_id=categoria_id,
                especificaciones=especificaciones,
                proveedor_preferido=proveedor,
                notas=notas,
                creado_por=request.user,
            )
            # Crear primer registro en historial
            HistorialPrecio.objects.create(
                item=item,
                precio=precio,
                moneda=moneda,
                observacion='Precio inicial',
                usuario=request.user,
            )
            messages.success(request, f'Ítem "{item.descripcion}" creado correctamente.')
            return redirect('bd_costos_lista')

        except ValueError:
            pass
        except InvalidOperation:
            messages.error(request, 'El precio ingresado no es válido.')

    context = {
        'categorias': categorias,
        'tipos': ItemCosto.TIPOS,
        'unidades': ItemCosto.UNIDADES,
        'accion': 'Crear',
    }
    return render(request, 'bd_costos/form_item.html', context)


@tenant_required
def editar_item_view(request, item_id):
    empresa = request.tenant
    item = get_object_or_404(ItemCosto, id=item_id, empresa=empresa)
    categorias = CategoriaItem.objects.filter(empresa=empresa, activo=True).order_by('codigo')

    if request.method == 'POST':
        try:
            descripcion = request.POST.get('descripcion', '').strip()
            tipo = request.POST.get('tipo', '')
            unidad = request.POST.get('unidad', 'un')
            unidad_custom = request.POST.get('unidad_custom', '').strip()
            precio_str = request.POST.get('precio_actual', '0').replace(',', '.')
            moneda = request.POST.get('moneda', 'USD')
            categoria_id = request.POST.get('categoria') or None
            especificaciones = request.POST.get('especificaciones', '').strip()
            proveedor = request.POST.get('proveedor_preferido', '').strip()
            notas = request.POST.get('notas', '').strip()
            activo = request.POST.get('activo') == 'on'

            nuevo_precio = Decimal(precio_str)
            if nuevo_precio <= 0:
                messages.error(request, 'El precio debe ser mayor que 0.')
                raise ValueError()

            # Registrar cambio de precio en historial
            if nuevo_precio != item.precio_actual:
                obs = request.POST.get('observacion_precio', '').strip() or 'Actualización de precio'
                HistorialPrecio.objects.create(
                    item=item,
                    precio=item.precio_actual,  # precio ANTERIOR
                    moneda=item.moneda,
                    observacion=f'Precio anterior antes del cambio: {obs}',
                    usuario=request.user,
                )

            item.descripcion = descripcion
            item.tipo = tipo
            item.unidad = unidad
            item.unidad_custom = unidad_custom
            item.precio_actual = nuevo_precio
            item.moneda = moneda
            item.categoria_id = categoria_id
            item.especificaciones = especificaciones
            item.proveedor_preferido = proveedor
            item.notas = notas
            item.activo = activo
            item.save()

            messages.success(request, f'Ítem "{item.descripcion}" actualizado.')
            return redirect('bd_costos_lista')

        except (ValueError, InvalidOperation):
            if not messages.get_messages(request):
                messages.error(request, 'Error al actualizar. Verifica los datos.')

    context = {
        'item': item,
        'categorias': categorias,
        'tipos': ItemCosto.TIPOS,
        'unidades': ItemCosto.UNIDADES,
        'accion': 'Editar',
    }
    return render(request, 'bd_costos/form_item.html', context)


@tenant_required
def historial_item_view(request, item_id):
    empresa = request.tenant
    item = get_object_or_404(ItemCosto, id=item_id, empresa=empresa)
    historial = HistorialPrecio.objects.filter(item=item).order_by('-fecha')

    # Para la gráfica Chart.js
    datos_grafica = [
        {
            'fecha': str(h.fecha),
            'precio': float(h.precio),
        }
        for h in reversed(list(historial))
    ]

    context = {
        'item': item,
        'historial': historial,
        'datos_grafica': json.dumps(datos_grafica),
    }
    return render(request, 'bd_costos/historial.html', context)


@tenant_required
@require_http_methods(['POST'])
def desactivar_item_view(request, item_id):
    empresa = request.tenant
    item = get_object_or_404(ItemCosto, id=item_id, empresa=empresa)
    item.activo = not item.activo
    item.save(update_fields=['activo'])
    estado = 'activado' if item.activo else 'desactivado'
    messages.success(request, f'Ítem "{item.descripcion}" {estado}.')
    return redirect('bd_costos_lista')


@tenant_required
def categorias_view(request):
    empresa = request.tenant
    categorias = CategoriaItem.objects.filter(empresa=empresa).order_by('codigo')

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        codigo = request.POST.get('codigo', '').strip().upper()
        padre_id = request.POST.get('padre') or None
        descripcion = request.POST.get('descripcion', '').strip()

        if not nombre or not codigo:
            messages.error(request, 'Nombre y código son requeridos.')
        elif CategoriaItem.objects.filter(empresa=empresa, codigo=codigo).exists():
            messages.error(request, f'Ya existe una categoría con código "{codigo}".')
        else:
            CategoriaItem.objects.create(
                empresa=empresa,
                nombre=nombre,
                codigo=codigo,
                padre_id=padre_id,
                descripcion=descripcion,
            )
            messages.success(request, f'Categoría "{nombre}" creada.')
            return redirect('bd_costos_categorias')

    # Construir árbol jerárquico
    categorias_raiz = categorias.filter(padre__isnull=True)
    context = {
        'categorias': categorias,
        'categorias_raiz': categorias_raiz,
    }
    return render(request, 'bd_costos/categorias.html', context)


@tenant_required
def buscar_items_api(request):
    """API endpoint para búsqueda de ítems (usado en cotizaciones)."""
    empresa = request.tenant
    q = request.GET.get('q', '').strip()

    items = ItemCosto.objects.filter(empresa=empresa, activo=True)
    if q:
        items = items.filter(
            Q(codigo__icontains=q) | Q(descripcion__icontains=q)
        )
    items = items.select_related('categoria')[:20]

    data = [
        {
            'id': str(item.id),
            'codigo': item.codigo,
            'descripcion': item.descripcion,
            'unidad': item.unidad_display,
            'precio': float(item.precio_actual),
            'moneda': item.moneda,
            'tipo': item.get_tipo_display(),
            'categoria': item.categoria.nombre if item.categoria else '',
        }
        for item in items
    ]
    return JsonResponse({'items': data})
