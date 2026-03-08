"""
Vistas de autenticación y dashboard principal.
"""
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Sum, Avg
from decimal import Decimal


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/dashboard/')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    empresa = request.tenant

    if empresa is None and not request.user.is_superuser:
        messages.warning(request, 'No tienes empresa asignada. Contacta al administrador.')
        return render(request, 'core/dashboard.html', {})

    # KPIs principales
    from apps.proyectos.models import Proyecto
    from apps.cotizaciones.models import Cotizacion

    proyectos = Proyecto.objects.filter(empresa=empresa) if empresa else Proyecto.objects.none()
    cotizaciones = Cotizacion.objects.filter(empresa=empresa) if empresa else Cotizacion.objects.none()

    # Stats
    proyectos_activos = proyectos.filter(
        estado__in=[Proyecto.ESTADO_PLANIFICACION, Proyecto.ESTADO_EN_EJECUCION, Proyecto.ESTADO_PAUSADO]
    )
    cotizaciones_pendientes = cotizaciones.filter(
        estado__in=[Cotizacion.ESTADO_BORRADOR, Cotizacion.ESTADO_ENVIADA]
    )
    proyectos_en_ejecucion = proyectos.filter(estado=Proyecto.ESTADO_EN_EJECUCION)

    valor_en_ejecucion = proyectos_en_ejecucion.aggregate(
        total=Sum('valor_contrato')
    )['total'] or Decimal('0.00')

    # Rentabilidad promedio (solo proyectos en ejecución y completados con datos)
    proyectos_lista = list(proyectos_activos.order_by('-fecha_creacion')[:10])

    # Alertas simples
    alertas = []
    for p in proyectos_lista:
        if p.esta_atrasado:
            dias = abs(p.dias_restantes)
            alertas.append({
                'tipo': 'danger',
                'mensaje': f'Proyecto "{p.nombre}" está atrasado {dias} días.',
                'url': f'/proyectos/{p.id}/'
            })
        if p.costo_real_total > p.valor_contrato:
            alertas.append({
                'tipo': 'warning',
                'mensaje': f'Proyecto "{p.nombre}" supera el valor del contrato.',
                'url': f'/proyectos/{p.id}/'
            })

    # Datos para gráfica (últimos 6 meses de cotizaciones)
    from django.utils import timezone
    from datetime import timedelta
    seis_meses_atras = timezone.now().date() - timedelta(days=180)

    cotizaciones_recientes = cotizaciones.filter(
        fecha_creacion__gte=seis_meses_atras
    ).order_by('fecha_creacion')

    context = {
        'proyectos_activos_count': proyectos_activos.count(),
        'cotizaciones_pendientes_count': cotizaciones_pendientes.count(),
        'valor_en_ejecucion': valor_en_ejecucion,
        'proyectos_lista': proyectos_lista,
        'cotizaciones_recientes_lista': list(cotizaciones_pendientes.order_by('-fecha_creacion')[:5]),
        'alertas': alertas,
    }
    return render(request, 'core/dashboard.html', context)
