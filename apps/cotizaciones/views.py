"""
Vistas del módulo Cotizaciones.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from decimal import Decimal, InvalidOperation
import datetime

from .models import Cotizacion, PartidaCotizacion
from apps.bd_costos.models import ItemCosto


def tenant_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.tenant:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return login_required(wrapper)


@tenant_required
def lista_view(request):
    empresa = request.tenant
    cotizaciones = Cotizacion.objects.filter(empresa=empresa).select_related('creado_por')

    # Filtros
    estado = request.GET.get('estado', '')
    busqueda = request.GET.get('q', '').strip()
    fecha_desde = request.GET.get('desde', '')
    fecha_hasta = request.GET.get('hasta', '')

    if estado:
        cotizaciones = cotizaciones.filter(estado=estado)
    if busqueda:
        cotizaciones = cotizaciones.filter(
            Q(numero__icontains=busqueda) |
            Q(cliente_nombre__icontains=busqueda) |
            Q(nombre_proyecto__icontains=busqueda)
        )
    if fecha_desde:
        cotizaciones = cotizaciones.filter(fecha_creacion__gte=fecha_desde)
    if fecha_hasta:
        cotizaciones = cotizaciones.filter(fecha_creacion__lte=fecha_hasta)

    cotizaciones = cotizaciones.order_by('-fecha_creacion')

    context = {
        'cotizaciones': cotizaciones,
        'estados': Cotizacion.ESTADOS,
        'estado_sel': estado,
        'busqueda': busqueda,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'total': cotizaciones.count(),
    }
    return render(request, 'cotizaciones/lista.html', context)


@tenant_required
def crear_view(request):
    empresa = request.tenant

    if not request.user.puede_editar_cotizaciones:
        messages.error(request, 'No tienes permisos para crear cotizaciones.')
        return redirect('cotizaciones_lista')

    if request.method == 'POST':
        return _guardar_cotizacion(request, empresa, None)

    # Fecha vencimiento default: hoy + 15 días
    fecha_vencimiento_default = (datetime.date.today() + datetime.timedelta(days=15)).strftime('%Y-%m-%d')

    context = {
        'accion': 'Nueva',
        'fecha_vencimiento_default': fecha_vencimiento_default,
        'margen_default': empresa.margen_utilidad_default,
        'terminos_default': empresa.terminos_condiciones_default,
    }
    return render(request, 'cotizaciones/form.html', context)


@tenant_required
def detalle_view(request, cot_id):
    empresa = request.tenant
    cot = get_object_or_404(Cotizacion, id=cot_id, empresa=empresa)
    partidas = cot.partidas.all().order_by('orden')

    context = {
        'cot': cot,
        'partidas': partidas,
    }
    return render(request, 'cotizaciones/detalle.html', context)


@tenant_required
def editar_view(request, cot_id):
    empresa = request.tenant
    cot = get_object_or_404(Cotizacion, id=cot_id, empresa=empresa)

    if not cot.puede_editarse:
        messages.error(request, f'La cotización {cot.numero} no puede editarse en su estado actual ({cot.get_estado_display()}).')
        return redirect('cotizacion_detalle', cot_id=cot_id)

    if not request.user.puede_editar_cotizaciones:
        messages.error(request, 'No tienes permisos para editar cotizaciones.')
        return redirect('cotizacion_detalle', cot_id=cot_id)

    if request.method == 'POST':
        return _guardar_cotizacion(request, empresa, cot)

    import json
    from decimal import Decimal as D
    partidas_qs = list(cot.partidas.all().order_by('orden').values(
        'id', 'orden', 'codigo', 'descripcion', 'unidad',
        'categoria', 'cantidad', 'precio_unitario', 'subtotal'
    ))
    # Convertir Decimal a float para serialización JSON
    for p in partidas_qs:
        p['cantidad'] = float(p['cantidad'])
        p['precio_unitario'] = float(p['precio_unitario'])
        p['subtotal'] = float(p['subtotal'])
        p['id'] = str(p['id'])

    context = {
        'accion': 'Editar',
        'cot': cot,
        'partidas_json': json.dumps(partidas_qs),
        'margen_default': cot.margen_utilidad_porcentaje,
        'terminos_default': cot.terminos_condiciones,
        'fecha_vencimiento_default': cot.fecha_vencimiento.strftime('%Y-%m-%d') if cot.fecha_vencimiento else (datetime.date.today() + datetime.timedelta(days=15)).strftime('%Y-%m-%d'),
    }
    return render(request, 'cotizaciones/form.html', context)


def _guardar_cotizacion(request, empresa, cot_existente):
    """Lógica común para crear y editar cotizaciones."""
    import json

    try:
        # Datos básicos
        cliente_nombre = request.POST.get('cliente_nombre', '').strip()
        cliente_rif = request.POST.get('cliente_rif', '').strip()
        cliente_direccion = request.POST.get('cliente_direccion', '').strip()
        cliente_telefono = request.POST.get('cliente_telefono', '').strip()
        cliente_email = request.POST.get('cliente_email', '').strip()
        cliente_contacto = request.POST.get('cliente_contacto', '').strip()
        nombre_proyecto = request.POST.get('nombre_proyecto', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        ubicacion = request.POST.get('ubicacion', '').strip()
        fecha_vencimiento_str = request.POST.get('fecha_vencimiento', '')
        margen_str = request.POST.get('margen_utilidad_porcentaje', '15').replace(',', '.')
        terminos = request.POST.get('terminos_condiciones', '').strip()
        notas_internas = request.POST.get('notas_internas', '').strip()

        if not cliente_nombre:
            messages.error(request, 'El nombre del cliente es requerido.')
            raise ValueError()
        if not nombre_proyecto:
            messages.error(request, 'El nombre del proyecto es requerido.')
            raise ValueError()
        if not fecha_vencimiento_str:
            messages.error(request, 'La fecha de vencimiento es requerida.')
            raise ValueError()

        fecha_vencimiento = datetime.date.fromisoformat(fecha_vencimiento_str)
        margen = Decimal(margen_str)

        # Partidas (enviadas como JSON)
        partidas_json = request.POST.get('partidas_data', '[]')
        partidas_data = json.loads(partidas_json)

        if not partidas_data:
            messages.error(request, 'Debes agregar al menos una partida.')
            raise ValueError()

        if cot_existente:
            cot = cot_existente
            cot.modificado_por = request.user
        else:
            cot = Cotizacion(empresa=empresa, creado_por=request.user)

        cot.cliente_nombre = cliente_nombre
        cot.cliente_rif = cliente_rif
        cot.cliente_direccion = cliente_direccion
        cot.cliente_telefono = cliente_telefono
        cot.cliente_email = cliente_email
        cot.cliente_contacto = cliente_contacto
        cot.nombre_proyecto = nombre_proyecto
        cot.descripcion = descripcion
        cot.ubicacion = ubicacion
        cot.fecha_vencimiento = fecha_vencimiento
        cot.margen_utilidad_porcentaje = margen
        cot.terminos_condiciones = terminos
        cot.notas_internas = notas_internas
        cot.save()

        # Eliminar partidas anteriores y recrear
        if cot_existente:
            cot.partidas.all().delete()

        subtotal_total = Decimal('0.00')
        for i, p_data in enumerate(partidas_data):
            cantidad = Decimal(str(p_data.get('cantidad', 0)))
            precio_unitario = Decimal(str(p_data.get('precio_unitario', 0)))
            subtotal = (cantidad * precio_unitario).quantize(Decimal('0.01'))
            subtotal_total += subtotal

            PartidaCotizacion.objects.create(
                cotizacion=cot,
                orden=i,
                codigo=p_data.get('codigo', '').strip(),
                descripcion=p_data.get('descripcion', '').strip(),
                unidad=p_data.get('unidad', 'un').strip(),
                categoria=p_data.get('categoria', '').strip(),
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal,
            )

        # Actualizar totales de la cotización (sin triggers)
        utilidad = (subtotal_total * margen / Decimal('100')).quantize(Decimal('0.01'))
        Cotizacion.objects.filter(id=cot.id).update(
            subtotal=subtotal_total,
            utilidad_monto=utilidad,
            total=subtotal_total + utilidad,
        )

        messages.success(request, f'Cotización {cot.numero} guardada correctamente.')
        return redirect('cotizacion_detalle', cot_id=cot.id)

    except ValueError:
        if not list(messages.get_messages(request)):
            messages.error(request, 'Error en los datos ingresados.')
        import json as _json
        # Intentar preservar las partidas que el usuario ingresó
        partidas_raw = request.POST.get('partidas_data', '[]')
        try:
            partidas_preservadas = _json.dumps(_json.loads(partidas_raw))
        except Exception:
            partidas_preservadas = '[]'
        ctx = {
            'accion': 'Editar' if cot_existente else 'Nueva',
            'cot': cot_existente,
            'partidas_json': partidas_preservadas,
            'margen_default': empresa.margen_utilidad_default,
            'terminos_default': empresa.terminos_condiciones_default,
            'fecha_vencimiento_default': (datetime.date.today() + datetime.timedelta(days=15)).strftime('%Y-%m-%d'),
        }
        return render(request, 'cotizaciones/form.html', ctx)


@tenant_required
@require_http_methods(['POST'])
def cambiar_estado_view(request, cot_id):
    empresa = request.tenant
    cot = get_object_or_404(Cotizacion, id=cot_id, empresa=empresa)
    nuevo_estado = request.POST.get('estado')

    estados_validos = [s[0] for s in Cotizacion.ESTADOS]
    if nuevo_estado not in estados_validos:
        messages.error(request, 'Estado no válido.')
        return redirect('cotizacion_detalle', cot_id=cot_id)

    # Validaciones de transición
    if nuevo_estado == Cotizacion.ESTADO_ENVIADA:
        if not cot.puede_editarse:
            messages.error(request, 'No se puede cambiar este estado.')
            return redirect('cotizacion_detalle', cot_id=cot_id)
        cot.fecha_envio = timezone.now()

    elif nuevo_estado in (Cotizacion.ESTADO_APROBADA, Cotizacion.ESTADO_RECHAZADA):
        if not request.user.puede_aprobar_cambios:
            messages.error(request, 'Solo Admins y Gerentes pueden aprobar cotizaciones.')
            return redirect('cotizacion_detalle', cot_id=cot_id)
        cot.fecha_respuesta = timezone.now()

    cot.estado = nuevo_estado
    cot.save(update_fields=['estado', 'fecha_envio', 'fecha_respuesta'])
    messages.success(request, f'Cotización cambiada a "{cot.get_estado_display()}".')
    return redirect('cotizacion_detalle', cot_id=cot_id)


@tenant_required
@require_http_methods(['POST'])
def convertir_proyecto_view(request, cot_id):
    """Convierte cotización aprobada en proyecto."""
    empresa = request.tenant
    cot = get_object_or_404(Cotizacion, id=cot_id, empresa=empresa)

    if cot.estado != Cotizacion.ESTADO_APROBADA:
        messages.error(request, 'Solo se pueden convertir cotizaciones aprobadas.')
        return redirect('cotizacion_detalle', cot_id=cot_id)

    if not request.user.puede_editar_cotizaciones:
        messages.error(request, 'No tienes permisos para convertir cotizaciones.')
        return redirect('cotizacion_detalle', cot_id=cot_id)

    try:
        fecha_inicio_str = request.POST.get('fecha_inicio', '')
        fecha_fin_str = request.POST.get('fecha_fin', '')

        if not fecha_inicio_str or not fecha_fin_str:
            messages.error(request, 'Las fechas de inicio y fin son requeridas.')
            return redirect('cotizacion_detalle', cot_id=cot_id)

        fecha_inicio = datetime.date.fromisoformat(fecha_inicio_str)
        fecha_fin = datetime.date.fromisoformat(fecha_fin_str)

        from apps.proyectos.models import Proyecto, PartidaProyecto

        # Crear proyecto
        proyecto = Proyecto.objects.create(
            empresa=empresa,
            cotizacion_origen=cot,
            nombre=cot.nombre_proyecto,
            descripcion=cot.descripcion,
            ubicacion=cot.ubicacion,
            cliente_nombre=cot.cliente_nombre,
            cliente_rif=cot.cliente_rif,
            cliente_contacto=cot.cliente_contacto,
            cliente_telefono=cot.cliente_telefono,
            cliente_email=cot.cliente_email,
            fecha_inicio_planeada=fecha_inicio,
            fecha_fin_planeada=fecha_fin,
            valor_contrato=cot.total,
            moneda=cot.moneda,
            estado=Proyecto.ESTADO_PLANIFICACION,
            gerente_proyecto=request.user,
            creado_por=request.user,
        )

        # Crear partidas del proyecto
        for partida in cot.partidas.all().order_by('orden'):
            PartidaProyecto.objects.create(
                proyecto=proyecto,
                orden=partida.orden,
                codigo=partida.codigo,
                descripcion=partida.descripcion,
                unidad=partida.unidad,
                categoria=partida.categoria,
                cantidad_presupuestada=partida.cantidad,
                precio_unitario_presupuestado=partida.precio_unitario,
                costo_presupuestado=partida.subtotal,
            )

        # Marcar cotización como convertida
        cot.estado = Cotizacion.ESTADO_CONVERTIDA
        cot.save(update_fields=['estado'])

        messages.success(request, f'Proyecto {proyecto.codigo} creado exitosamente.')
        return redirect('proyecto_detalle', proyecto_id=proyecto.id)

    except Exception as e:
        messages.error(request, f'Error al crear el proyecto: {str(e)}')
        return redirect('cotizacion_detalle', cot_id=cot_id)


@tenant_required
@require_http_methods(['POST'])
def duplicar_view(request, cot_id):
    """Duplica una cotización como borrador."""
    empresa = request.tenant
    cot = get_object_or_404(Cotizacion, id=cot_id, empresa=empresa)

    nueva = Cotizacion.objects.create(
        empresa=empresa,
        cliente_nombre=cot.cliente_nombre,
        cliente_rif=cot.cliente_rif,
        cliente_direccion=cot.cliente_direccion,
        cliente_telefono=cot.cliente_telefono,
        cliente_email=cot.cliente_email,
        cliente_contacto=cot.cliente_contacto,
        nombre_proyecto=f'{cot.nombre_proyecto} (Copia)',
        descripcion=cot.descripcion,
        ubicacion=cot.ubicacion,
        fecha_vencimiento=datetime.date.today() + datetime.timedelta(days=15),
        margen_utilidad_porcentaje=cot.margen_utilidad_porcentaje,
        terminos_condiciones=cot.terminos_condiciones,
        estado=Cotizacion.ESTADO_BORRADOR,
        creado_por=request.user,
    )

    for partida in cot.partidas.all().order_by('orden'):
        PartidaCotizacion.objects.create(
            cotizacion=nueva,
            orden=partida.orden,
            codigo=partida.codigo,
            descripcion=partida.descripcion,
            unidad=partida.unidad,
            categoria=partida.categoria,
            cantidad=partida.cantidad,
            precio_unitario=partida.precio_unitario,
            subtotal=partida.subtotal,
        )

    nueva.calcular_totales()
    Cotizacion.objects.filter(id=nueva.id).update(
        subtotal=nueva.subtotal,
        utilidad_monto=nueva.utilidad_monto,
        total=nueva.total,
    )

    messages.success(request, f'Cotización duplicada como {nueva.numero}.')
    return redirect('cotizacion_editar', cot_id=nueva.id)


@tenant_required
def pdf_view(request, cot_id):
    """Genera PDF de la cotización."""
    empresa = request.tenant
    cot = get_object_or_404(Cotizacion, id=cot_id, empresa=empresa)

    try:
        from .pdf_generator import generar_pdf_cotizacion
        pdf_buffer = generar_pdf_cotizacion(cot)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{cot.numero}.pdf"'
        return response
    except ImportError:
        messages.warning(request, 'PDF no disponible. Instala WeasyPrint o ReportLab.')
        return redirect('cotizacion_detalle', cot_id=cot_id)
    except Exception as e:
        messages.error(request, f'Error al generar PDF: {str(e)}')
        return redirect('cotizacion_detalle', cot_id=cot_id)
