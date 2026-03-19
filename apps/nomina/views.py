"""
Vistas del módulo Nómina / Horas Hombre.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum
from decimal import Decimal, InvalidOperation

from .models import CargoTrabajador, HistorialCostoHH, RegistroHH


def tenant_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.tenant:
            messages.error(request, 'No tienes empresa asignada.')
            return redirect('login')
        if not request.user.puede_ver_costos:
            messages.error(request, 'No tienes permisos para acceder a Nómina.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return login_required(wrapper)


@tenant_required
def lista_cargos_view(request):
    empresa = request.tenant
    cargos = CargoTrabajador.objects.filter(empresa=empresa)

    busqueda = request.GET.get('q', '').strip()
    nivel = request.GET.get('nivel', '')
    solo_activos = request.GET.get('activo', 'true')

    if busqueda:
        cargos = cargos.filter(
            Q(codigo__icontains=busqueda) |
            Q(nombre__icontains=busqueda)
        )
    if nivel:
        cargos = cargos.filter(nivel=nivel)
    if solo_activos != 'todos':
        cargos = cargos.filter(activo=(solo_activos == 'true'))

    context = {
        'cargos': cargos,
        'niveles': CargoTrabajador.NIVEL_CHOICES,
        'busqueda': busqueda,
        'nivel_sel': nivel,
        'activo_sel': solo_activos,
        'total_cargos': cargos.count(),
    }
    return render(request, 'nomina/lista_cargos.html', context)


@tenant_required
def crear_cargo_view(request):
    empresa = request.tenant

    if request.method == 'POST':
        return _guardar_cargo(request, empresa)

    context = {
        'niveles': CargoTrabajador.NIVEL_CHOICES,
        'accion': 'Crear',
    }
    return render(request, 'nomina/form_cargo.html', context)


@tenant_required
def editar_cargo_view(request, cargo_id):
    empresa = request.tenant
    cargo = get_object_or_404(CargoTrabajador, id=cargo_id, empresa=empresa)

    if request.method == 'POST':
        return _guardar_cargo(request, empresa, cargo)

    context = {
        'cargo': cargo,
        'niveles': CargoTrabajador.NIVEL_CHOICES,
        'accion': 'Editar',
    }
    return render(request, 'nomina/form_cargo.html', context)


@tenant_required
def detalle_cargo_view(request, cargo_id):
    empresa = request.tenant
    cargo = get_object_or_404(CargoTrabajador, id=cargo_id, empresa=empresa)
    historial = HistorialCostoHH.objects.filter(cargo=cargo)

    # Estadísticas de uso
    registros = RegistroHH.objects.filter(cargo=cargo)
    total_horas = registros.aggregate(total=Sum('horas'))['total'] or Decimal('0')
    total_costo = registros.aggregate(total=Sum('costo_total'))['total'] or Decimal('0')

    context = {
        'cargo': cargo,
        'historial': historial,
        'total_horas': total_horas,
        'total_costo': total_costo,
        'total_registros': registros.count(),
    }
    return render(request, 'nomina/detalle_cargo.html', context)


@tenant_required
def registrar_hh_view(request, partida_id):
    """Registrar horas hombre en una partida de proyecto."""
    from apps.proyectos.models import PartidaProyecto
    empresa = request.tenant
    partida = get_object_or_404(PartidaProyecto, id=partida_id, proyecto__empresa=empresa)
    proyecto = partida.proyecto

    cargos = CargoTrabajador.objects.filter(empresa=empresa, activo=True)

    if request.method == 'POST':
        try:
            cargo_id = request.POST.get('cargo')
            fecha_str = request.POST.get('fecha', '').strip()
            cantidad_str = request.POST.get('cantidad_trabajadores', '1')
            horas_str = request.POST.get('horas', '0').replace(',', '.')
            observaciones = request.POST.get('observaciones', '').strip()

            if not cargo_id:
                messages.error(request, 'Debes seleccionar un cargo.')
                raise ValueError()
            if not fecha_str:
                messages.error(request, 'La fecha es requerida.')
                raise ValueError()

            import datetime
            fecha = datetime.date.fromisoformat(fecha_str)
            if fecha > datetime.date.today():
                messages.error(request, 'No puedes registrar horas en una fecha futura.')
                raise ValueError()

            cargo = get_object_or_404(CargoTrabajador, id=cargo_id, empresa=empresa)
            cantidad = int(cantidad_str)
            horas = Decimal(horas_str)

            if cantidad < 1:
                messages.error(request, 'La cantidad de trabajadores debe ser al menos 1.')
                raise ValueError()
            if horas <= 0:
                messages.error(request, 'Las horas deben ser mayores que 0.')
                raise ValueError()

            RegistroHH.objects.create(
                partida=partida,
                cargo=cargo,
                fecha=fecha,
                cantidad_trabajadores=cantidad,
                horas=horas,
                costo_hora_aplicado=cargo.costo_hora,
                observaciones=observaciones,
                registrado_por=request.user,
            )
            messages.success(request, f'Registradas {horas}h × {cantidad} {cargo.nombre}.')
            return redirect('proyecto_detalle', proyecto_id=proyecto.id)

        except (ValueError, InvalidOperation):
            if not list(messages.get_messages(request)):
                messages.error(request, 'Error al registrar. Verifica los datos.')

    # Registros existentes de esta partida
    registros = RegistroHH.objects.filter(partida=partida)
    total_hh_costo = registros.aggregate(total=Sum('costo_total'))['total'] or Decimal('0')

    context = {
        'partida': partida,
        'proyecto': proyecto,
        'cargos': cargos,
        'registros': registros,
        'total_hh_costo': total_hh_costo,
    }
    return render(request, 'nomina/registrar_hh.html', context)


@tenant_required
def buscar_cargos_api(request):
    """API JSON para búsqueda de cargos."""
    empresa = request.tenant
    q = request.GET.get('q', '').strip()

    cargos = CargoTrabajador.objects.filter(empresa=empresa, activo=True)
    if q:
        cargos = cargos.filter(
            Q(codigo__icontains=q) | Q(nombre__icontains=q)
        )
    cargos = cargos[:20]

    data = [
        {
            'id': str(c.id),
            'codigo': c.codigo,
            'nombre': c.nombre,
            'nivel': c.get_nivel_display(),
            'costo_hora': float(c.costo_hora),
        }
        for c in cargos
    ]
    return JsonResponse({'cargos': data})


def _guardar_cargo(request, empresa, cargo=None):
    """Lógica compartida para crear/editar cargo."""
    try:
        codigo = request.POST.get('codigo', '').strip().upper()
        nombre = request.POST.get('nombre', '').strip()
        nivel = request.POST.get('nivel', 'OFICIAL')
        descripcion = request.POST.get('descripcion', '').strip()
        costo_hora_str = request.POST.get('costo_hora', '0').replace(',', '.')
        moneda = request.POST.get('moneda', 'USD')
        sincronizar = request.POST.get('sincronizar_bd') == 'on'

        if not codigo:
            messages.error(request, 'El código es requerido.')
            raise ValueError()
        if not nombre:
            messages.error(request, 'El nombre del cargo es requerido.')
            raise ValueError()

        costo_hora = Decimal(costo_hora_str)
        if costo_hora <= 0:
            messages.error(request, 'El costo por hora debe ser mayor que 0.')
            raise ValueError()

        # Verificar código único
        qs = CargoTrabajador.objects.filter(empresa=empresa, codigo=codigo)
        if cargo:
            qs = qs.exclude(id=cargo.id)
        if qs.exists():
            messages.error(request, f'Ya existe un cargo con el código "{codigo}".')
            raise ValueError()

        es_nuevo = cargo is None
        costo_anterior = None if es_nuevo else cargo.costo_hora

        if es_nuevo:
            cargo = CargoTrabajador(empresa=empresa)

        cargo.codigo = codigo
        cargo.nombre = nombre
        cargo.nivel = nivel
        cargo.descripcion = descripcion
        cargo.costo_hora = costo_hora
        cargo.moneda = moneda
        cargo.save()

        # Registrar cambio en historial si hubo cambio de costo
        if not es_nuevo and costo_anterior != costo_hora:
            HistorialCostoHH.objects.create(
                cargo=cargo,
                costo_hora_anterior=costo_anterior,
                costo_hora_nuevo=costo_hora,
                observacion=request.POST.get('observacion_cambio', '').strip() or 'Actualización de tarifa',
                usuario=request.user,
            )

        # Sincronizar con BD de Costos si se pidió
        if sincronizar:
            cargo.sincronizar_item_costo()
            messages.info(request, 'Sincronizado con BD de Costos.')

        accion = 'creado' if es_nuevo else 'actualizado'
        messages.success(request, f'Cargo "{cargo.nombre}" {accion} correctamente.')
        return redirect('nomina_detalle', cargo_id=cargo.id)

    except (ValueError, InvalidOperation):
        if not list(messages.get_messages(request)):
            messages.error(request, 'Error al guardar. Verifica los datos.')
        context = {
            'cargo': cargo,
            'niveles': CargoTrabajador.NIVEL_CHOICES,
            'accion': 'Editar' if cargo else 'Crear',
        }
        return render(request, 'nomina/form_cargo.html', context)
