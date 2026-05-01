"""
Vistas del módulo Proyectos en Ejecución.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from decimal import Decimal
import datetime

from .models import Proyecto, PartidaProyecto, RegistroAvance, FotoProyecto, OrdenCambio


from apps.core.decorators import tenant_required


@tenant_required
def lista_view(request):
    empresa = request.tenant
    proyectos = Proyecto.objects.filter(empresa=empresa).select_related(
        'gerente_proyecto', 'supervisor'
    ).prefetch_related('partidas')

    estado = request.GET.get('estado', '')
    if estado:
        proyectos = proyectos.filter(estado=estado)

    proyectos = proyectos.order_by('-fecha_creacion')

    context = {
        'proyectos': proyectos,
        'estados': Proyecto.ESTADOS,
        'estado_sel': estado,
    }
    return render(request, 'proyectos/lista.html', context)


@tenant_required
def detalle_view(request, proyecto_id):
    empresa = request.tenant
    proyecto = get_object_or_404(Proyecto, id=proyecto_id, empresa=empresa)

    # Verificar acceso del supervisor: solo sus proyectos
    if (request.user.rol == 'SUPERVISOR' and
            proyecto.supervisor != request.user and
            proyecto.gerente_proyecto != request.user):
        messages.error(request, 'No tienes acceso a este proyecto.')
        return redirect('proyectos_lista')

    partidas = proyecto.partidas.all().order_by('orden')
    fotos = proyecto.fotos.all().order_by('-fecha')[:12]
    ordenes_cambio = proyecto.ordenes_cambio.all().order_by('numero')

    context = {
        'proyecto': proyecto,
        'partidas': partidas,
        'fotos': fotos,
        'ordenes_cambio': ordenes_cambio,
        'tab_activo': request.GET.get('tab', 'resumen'),
    }
    return render(request, 'proyectos/detalle.html', context)


@tenant_required
@require_http_methods(['POST'])
def cambiar_estado_view(request, proyecto_id):
    empresa = request.tenant
    proyecto = get_object_or_404(Proyecto, id=proyecto_id, empresa=empresa)

    if not request.user.puede_editar_cotizaciones:
        messages.error(request, 'No tienes permisos.')
        return redirect('proyecto_detalle', proyecto_id=proyecto_id)

    nuevo_estado = request.POST.get('estado')
    estados_validos = [s[0] for s in Proyecto.ESTADOS]
    if nuevo_estado not in estados_validos:
        messages.error(request, 'Estado no válido.')
        return redirect('proyecto_detalle', proyecto_id=proyecto_id)

    update_fields = ['estado']

    if nuevo_estado == Proyecto.ESTADO_EN_EJECUCION and not proyecto.fecha_inicio_real:
        proyecto.fecha_inicio_real = datetime.date.today()
        update_fields.append('fecha_inicio_real')

    if nuevo_estado == Proyecto.ESTADO_COMPLETADO and not proyecto.fecha_fin_real:
        proyecto.fecha_fin_real = datetime.date.today()
        update_fields.append('fecha_fin_real')

    proyecto.estado = nuevo_estado
    proyecto.save(update_fields=update_fields)
    messages.success(request, f'Proyecto actualizado a "{proyecto.get_estado_display()}".')
    return redirect('proyecto_detalle', proyecto_id=proyecto_id)


@tenant_required
@require_http_methods(['GET', 'POST'])
def registrar_avance_view(request, proyecto_id, partida_id):
    empresa = request.tenant
    proyecto = get_object_or_404(Proyecto, id=proyecto_id, empresa=empresa)
    partida = get_object_or_404(PartidaProyecto, id=partida_id, proyecto=proyecto)

    if request.method == 'POST':
        try:
            fecha_str = request.POST.get('fecha', str(datetime.date.today()))
            cantidad_str = request.POST.get('cantidad_ejecutada_dia', '0').replace(',', '.')
            costo_str = request.POST.get('costo_dia', '0').replace(',', '.')
            observaciones = request.POST.get('observaciones', '').strip()

            fecha = datetime.date.fromisoformat(fecha_str)
            if fecha > datetime.date.today():
                messages.error(request, 'La fecha no puede ser futura.')
                raise ValueError()

            cantidad = Decimal(cantidad_str)
            costo = Decimal(costo_str)

            if cantidad <= 0:
                messages.error(request, 'La cantidad debe ser mayor que 0.')
                raise ValueError()
            if costo < 0:
                messages.error(request, 'El costo no puede ser negativo.')
                raise ValueError()

            RegistroAvance.objects.create(
                partida=partida,
                fecha=fecha,
                cantidad_ejecutada_dia=cantidad,
                costo_dia=costo,
                observaciones=observaciones,
                registrado_por=request.user,
            )

            messages.success(request, f'Avance registrado: {cantidad} {partida.unidad} — ${costo}')
            return redirect('proyecto_detalle', proyecto_id=proyecto_id)

        except ValueError:
            pass
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    registros_previos = RegistroAvance.objects.filter(partida=partida).order_by('-fecha')[:5]

    context = {
        'proyecto': proyecto,
        'partida': partida,
        'registros_previos': registros_previos,
        'hoy': datetime.date.today(),
    }
    return render(request, 'proyectos/registrar_avance.html', context)


@tenant_required
@require_http_methods(['POST'])
def subir_fotos_view(request, proyecto_id):
    empresa = request.tenant
    proyecto = get_object_or_404(Proyecto, id=proyecto_id, empresa=empresa)

    fotos = request.FILES.getlist('fotos')
    descripcion = request.POST.get('descripcion', 'Foto de avance').strip()

    if not fotos:
        messages.error(request, 'No se recibieron fotos.')
        return redirect('proyecto_detalle', proyecto_id=proyecto_id)

    count = 0
    for foto in fotos[:10]:  # max 10 fotos
        if foto.size > 5 * 1024 * 1024:  # 5MB
            messages.warning(request, f'Foto "{foto.name}" supera 5MB y fue omitida.')
            continue
        FotoProyecto.objects.create(
            proyecto=proyecto,
            descripcion=descripcion,
            imagen=foto,
            subido_por=request.user,
        )
        count += 1

    if count > 0:
        messages.success(request, f'{count} foto{"s" if count > 1 else ""} subida{"s" if count > 1 else ""} correctamente.')
    return redirect('proyecto_detalle', proyecto_id=proyecto_id)


@tenant_required
@require_http_methods(['GET', 'POST'])
def orden_cambio_view(request, proyecto_id):
    empresa = request.tenant
    proyecto = get_object_or_404(Proyecto, id=proyecto_id, empresa=empresa)

    if not request.user.puede_editar_cotizaciones:
        messages.error(request, 'No tienes permisos.')
        return redirect('proyecto_detalle', proyecto_id=proyecto_id)

    if request.method == 'POST':
        try:
            descripcion = request.POST.get('descripcion', '').strip()
            justificacion = request.POST.get('justificacion', '').strip()
            impacto_costo_str = request.POST.get('impacto_costo', '0').replace(',', '.')
            impacto_tiempo_str = request.POST.get('impacto_tiempo_dias', '0')

            if not descripcion:
                messages.error(request, 'La descripción es requerida.')
                raise ValueError()

            # Número secuencial
            from django.db.models import Max
            ultimo = proyecto.ordenes_cambio.aggregate(max_num=Max('numero'))['max_num'] or 0

            OrdenCambio.objects.create(
                proyecto=proyecto,
                numero=ultimo + 1,
                descripcion=descripcion,
                justificacion=justificacion,
                impacto_costo=Decimal(impacto_costo_str),
                impacto_tiempo_dias=int(impacto_tiempo_str),
                solicitado_por=request.user,
            )
            messages.success(request, 'Orden de cambio creada.')
            return redirect('proyecto_detalle', proyecto_id=proyecto_id)

        except ValueError:
            pass

    return redirect('proyecto_detalle', proyecto_id=proyecto_id)


@tenant_required
@require_http_methods(['POST'])
def aprobar_orden_cambio_view(request, proyecto_id, oc_id):
    empresa = request.tenant
    proyecto = get_object_or_404(Proyecto, id=proyecto_id, empresa=empresa)
    oc = get_object_or_404(OrdenCambio, id=oc_id, proyecto=proyecto)

    if not request.user.puede_aprobar_cambios:
        messages.error(request, 'Solo Admins y Gerentes pueden aprobar órdenes de cambio.')
        return redirect('proyecto_detalle', proyecto_id=proyecto_id)

    if oc.estado != OrdenCambio.ESTADO_PENDIENTE:
        messages.error(request, 'Esta orden ya fue procesada.')
        return redirect('proyecto_detalle', proyecto_id=proyecto_id)

    accion = request.POST.get('accion')
    observaciones = request.POST.get('observaciones', '').strip()

    if accion == 'aprobar':
        oc.aprobar(request.user, observaciones)
        messages.success(request, f'Orden de cambio OC-{str(oc.numero).zfill(3)} aprobada.')
    elif accion == 'rechazar':
        oc.rechazar(request.user, observaciones)
        messages.success(request, f'Orden de cambio OC-{str(oc.numero).zfill(3)} rechazada.')
    else:
        messages.error(request, 'Acción no válida.')

    return redirect('proyecto_detalle', proyecto_id=proyecto_id)
