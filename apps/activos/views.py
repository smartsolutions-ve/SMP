"""
Vistas del módulo Activos del Cliente.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import datetime

from .models import ActivoCliente


from apps.core.decorators import tenant_required


@tenant_required
def lista_view(request):
    empresa = request.tenant
    activos = ActivoCliente.objects.filter(empresa=empresa)

    # Filtros
    busqueda = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')
    cliente = request.GET.get('cliente', '')
    solo_activos = request.GET.get('activo', 'true')

    if busqueda:
        activos = activos.filter(
            Q(codigo_equipo__icontains=busqueda) |
            Q(nombre__icontains=busqueda) |
            Q(marca__icontains=busqueda) |
            Q(serial__icontains=busqueda) |
            Q(ubicacion__icontains=busqueda)
        )
    if tipo:
        activos = activos.filter(tipo=tipo)
    if estado:
        activos = activos.filter(estado=estado)
    if cliente:
        activos = activos.filter(cliente_nombre__icontains=cliente)
    if solo_activos != 'todos':
        activos = activos.filter(activo=(solo_activos == 'true'))

    # Estadísticas rápidas
    total = activos.count()
    operativos = activos.filter(estado='OPERATIVO').count()
    requieren_mtto = sum(1 for a in activos if a.requiere_mtto)

    # Lista de clientes únicos para filtro
    clientes_unicos = (ActivoCliente.objects
        .filter(empresa=empresa, activo=True)
        .values_list('cliente_nombre', flat=True)
        .distinct()
        .order_by('cliente_nombre'))

    context = {
        'activos': activos,
        'tipos': ActivoCliente.TIPO_CHOICES,
        'estados': ActivoCliente.ESTADO_CHOICES,
        'clientes_unicos': clientes_unicos,
        'busqueda': busqueda,
        'tipo_sel': tipo,
        'estado_sel': estado,
        'cliente_sel': cliente,
        'activo_sel': solo_activos,
        'total': total,
        'operativos': operativos,
        'requieren_mtto': requieren_mtto,
    }
    return render(request, 'activos/lista.html', context)


@tenant_required
def crear_view(request):
    empresa = request.tenant

    if request.method == 'POST':
        return _guardar_activo(request, empresa)

    context = {
        'tipos': ActivoCliente.TIPO_CHOICES,
        'estados': ActivoCliente.ESTADO_CHOICES,
        'accion': 'Registrar',
    }
    return render(request, 'activos/form.html', context)


@tenant_required
def editar_view(request, activo_id):
    empresa = request.tenant
    activo = get_object_or_404(ActivoCliente, id=activo_id, empresa=empresa)

    if request.method == 'POST':
        return _guardar_activo(request, empresa, activo)

    context = {
        'activo': activo,
        'tipos': ActivoCliente.TIPO_CHOICES,
        'estados': ActivoCliente.ESTADO_CHOICES,
        'accion': 'Editar',
    }
    return render(request, 'activos/form.html', context)


@tenant_required
def detalle_view(request, activo_id):
    empresa = request.tenant
    activo = get_object_or_404(ActivoCliente, id=activo_id, empresa=empresa)

    # Cotizaciones y proyectos asociados
    cotizaciones = activo.cotizaciones.all().order_by('-fecha_creacion') if hasattr(activo, 'cotizaciones') else []
    proyectos = activo.proyectos.all().order_by('-fecha_creacion') if hasattr(activo, 'proyectos') else []

    context = {
        'activo': activo,
        'cotizaciones': cotizaciones,
        'proyectos': proyectos,
    }
    return render(request, 'activos/detalle.html', context)


@tenant_required
def buscar_api(request):
    """API JSON para buscar activos (usado en formularios de cotización/proyecto)."""
    empresa = request.tenant
    q = request.GET.get('q', '').strip()

    activos = ActivoCliente.objects.filter(empresa=empresa, activo=True)
    if q:
        activos = activos.filter(
            Q(codigo_equipo__icontains=q) |
            Q(nombre__icontains=q) |
            Q(cliente_nombre__icontains=q) |
            Q(serial__icontains=q)
        )
    activos = activos[:20]

    data = [
        {
            'id': str(a.id),
            'codigo': a.codigo_equipo,
            'nombre': a.nombre,
            'tipo': a.get_tipo_display(),
            'cliente': a.cliente_nombre,
            'ubicacion': a.ubicacion,
            'estado': a.get_estado_display(),
        }
        for a in activos
    ]
    return JsonResponse({'activos': data})


def _guardar_activo(request, empresa, activo=None):
    """Lógica compartida para crear/editar activo."""
    try:
        codigo = request.POST.get('codigo_equipo', '').strip().upper()
        nombre = request.POST.get('nombre', '').strip()
        tipo = request.POST.get('tipo', 'OTRO')
        marca = request.POST.get('marca', '').strip()
        modelo = request.POST.get('modelo', '').strip()
        serial = request.POST.get('serial', '').strip()
        ubicacion = request.POST.get('ubicacion', '').strip()
        area = request.POST.get('area', '').strip()
        cliente_nombre = request.POST.get('cliente_nombre', '').strip()
        cliente_rif = request.POST.get('cliente_rif', '').strip()
        estado = request.POST.get('estado', 'OPERATIVO')
        fecha_instalacion_str = request.POST.get('fecha_instalacion', '').strip()
        frecuencia_str = request.POST.get('frecuencia_mtto_dias', '').strip()
        proximo_mtto_str = request.POST.get('proximo_mtto', '').strip()
        especificaciones = request.POST.get('especificaciones', '').strip()
        notas = request.POST.get('notas', '').strip()

        # Validaciones
        if not codigo:
            messages.error(request, 'El código/TAG es requerido.')
            raise ValueError()
        if not nombre:
            messages.error(request, 'El nombre del equipo es requerido.')
            raise ValueError()
        if not cliente_nombre:
            messages.error(request, 'El nombre del cliente propietario es requerido.')
            raise ValueError()

        # Verificar código único
        qs = ActivoCliente.objects.filter(empresa=empresa, codigo_equipo=codigo)
        if activo:
            qs = qs.exclude(id=activo.id)
        if qs.exists():
            messages.error(request, f'Ya existe un activo con el código "{codigo}".')
            raise ValueError()

        # Parsear fechas
        fecha_instalacion = None
        if fecha_instalacion_str:
            fecha_instalacion = datetime.date.fromisoformat(fecha_instalacion_str)

        frecuencia = None
        if frecuencia_str:
            frecuencia = int(frecuencia_str)

        proximo_mtto = None
        if proximo_mtto_str:
            proximo_mtto = datetime.date.fromisoformat(proximo_mtto_str)

        es_nuevo = activo is None
        if es_nuevo:
            activo = ActivoCliente(
                empresa=empresa,
                creado_por=request.user,
            )

        activo.codigo_equipo = codigo
        activo.nombre = nombre
        activo.tipo = tipo
        activo.marca = marca
        activo.modelo = modelo
        activo.serial = serial
        activo.ubicacion = ubicacion
        activo.area = area
        activo.cliente_nombre = cliente_nombre
        activo.cliente_rif = cliente_rif
        activo.estado = estado
        activo.fecha_instalacion = fecha_instalacion
        activo.frecuencia_mtto_dias = frecuencia
        activo.proximo_mtto = proximo_mtto
        activo.especificaciones = especificaciones
        activo.notas = notas
        activo.save()

        accion = 'registrado' if es_nuevo else 'actualizado'
        messages.success(request, f'Activo "{activo.nombre}" {accion} correctamente.')
        return redirect('activos_detalle', activo_id=activo.id)

    except ValueError:
        context = {
            'activo': activo,
            'tipos': ActivoCliente.TIPO_CHOICES,
            'estados': ActivoCliente.ESTADO_CHOICES,
            'accion': 'Editar' if activo else 'Registrar',
        }
        return render(request, 'activos/form.html', context)
