"""
Vistas del módulo Reportes.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg, Q
from decimal import Decimal
import datetime
import json


def tenant_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.tenant:
            return redirect('login')
        if not request.user.puede_ver_costos:
            messages.error(request, 'No tienes permisos para ver reportes.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return login_required(wrapper)


@tenant_required
def lista_view(request):
    empresa = request.tenant
    from apps.proyectos.models import Proyecto
    from apps.cotizaciones.models import Cotizacion

    # Rango de fechas (default: último año)
    hoy = datetime.date.today()
    fecha_desde_str = request.GET.get('desde', (hoy - datetime.timedelta(days=365)).strftime('%Y-%m-%d'))
    fecha_hasta_str = request.GET.get('hasta', hoy.strftime('%Y-%m-%d'))
    try:
        fecha_desde = datetime.date.fromisoformat(fecha_desde_str)
        fecha_hasta = datetime.date.fromisoformat(fecha_hasta_str)
    except ValueError:
        fecha_desde = hoy - datetime.timedelta(days=365)
        fecha_hasta = hoy

    # Proyectos en el período
    proyectos = Proyecto.objects.filter(
        empresa=empresa,
        fecha_creacion__date__gte=fecha_desde,
        fecha_creacion__date__lte=fecha_hasta,
    ).prefetch_related('partidas')

    # Cotizaciones en el período
    cotizaciones = Cotizacion.objects.filter(
        empresa=empresa,
        fecha_creacion__gte=fecha_desde,
        fecha_creacion__lte=fecha_hasta,
    )

    # === REPORTE 1: Rentabilidad por proyecto ===
    datos_rentabilidad = []
    total_valor = Decimal('0')
    total_costo = Decimal('0')
    total_utilidad = Decimal('0')

    for p in proyectos:
        costo = p.costo_real_total
        utilidad = p.utilidad_real
        margen = p.margen_real_porcentaje
        datos_rentabilidad.append({
            'codigo': p.codigo,
            'nombre': p.nombre[:35],
            'cliente': p.cliente_nombre[:25],
            'estado': p.get_estado_display(),
            'valor_contrato': p.valor_contrato,
            'costo_real': costo,
            'utilidad': utilidad,
            'margen': margen,
            'rentable': utilidad >= 0,
        })
        total_valor += p.valor_contrato
        total_costo += costo
        total_utilidad += utilidad

    margen_promedio = (total_utilidad / total_valor * 100).quantize(Decimal('0.01')) if total_valor > 0 else Decimal('0')

    # === REPORTE 2: Análisis de cotizaciones ===
    total_cot = cotizaciones.count()
    cot_aprobadas = cotizaciones.filter(estado__in=['APROBADA', 'CONVERTIDA']).count()
    cot_rechazadas = cotizaciones.filter(estado='RECHAZADA').count()
    cot_pendientes = cotizaciones.filter(estado__in=['BORRADOR', 'ENVIADA']).count()
    tasa_conversion = round(cot_aprobadas / total_cot * 100, 1) if total_cot > 0 else 0

    valor_cotizaciones = cotizaciones.filter(
        estado__in=['APROBADA', 'CONVERTIDA']
    ).aggregate(total=Sum('total'))['total'] or Decimal('0')

    # Distribución de estados para gráfica
    estados_cotizacion = []
    for estado_val, estado_label in [('BORRADOR','Borrador'),('ENVIADA','Enviada'),
                                      ('APROBADA','Aprobada'),('RECHAZADA','Rechazada'),
                                      ('CONVERTIDA','Convertida')]:
        cnt = cotizaciones.filter(estado=estado_val).count()
        if cnt > 0:
            estados_cotizacion.append({'label': estado_label, 'count': cnt})

    # Gráfica: rentabilidad por proyecto (para Chart.js)
    grafica_labels = [d['codigo'] for d in datos_rentabilidad]
    grafica_valor = [float(d['valor_contrato']) for d in datos_rentabilidad]
    grafica_costo = [float(d['costo_real']) for d in datos_rentabilidad]
    grafica_utilidad = [float(d['utilidad']) for d in datos_rentabilidad]

    context = {
        'fecha_desde': fecha_desde.strftime('%Y-%m-%d'),
        'fecha_hasta': fecha_hasta.strftime('%Y-%m-%d'),
        'datos_rentabilidad': datos_rentabilidad,
        'total_valor': total_valor,
        'total_costo': total_costo,
        'total_utilidad': total_utilidad,
        'margen_promedio': margen_promedio,
        'total_proyectos': proyectos.count(),
        # Cotizaciones
        'total_cot': total_cot,
        'cot_aprobadas': cot_aprobadas,
        'cot_rechazadas': cot_rechazadas,
        'cot_pendientes': cot_pendientes,
        'tasa_conversion': tasa_conversion,
        'valor_cotizaciones': valor_cotizaciones,
        'estados_cotizacion': json.dumps(estados_cotizacion),
        # Gráficas
        'grafica_labels': json.dumps(grafica_labels),
        'grafica_valor': json.dumps(grafica_valor),
        'grafica_costo': json.dumps(grafica_costo),
        'grafica_utilidad': json.dumps(grafica_utilidad),
    }
    return render(request, 'reportes/lista.html', context)
