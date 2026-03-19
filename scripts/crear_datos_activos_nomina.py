"""
Script para crear datos demo de Activos y Nómina.
Ejecutar: cd smart_pm && USE_SQLITE=true DJANGO_SETTINGS_MODULE=config.settings.development ../env/bin/python manage.py shell < scripts/crear_datos_activos_nomina.py
"""
import datetime
from decimal import Decimal

# Importar modelos
from apps.core.models import Empresa, Usuario
from apps.activos.models import ActivoCliente
from apps.nomina.models import CargoTrabajador

# Obtener empresa y usuario
empresa = Empresa.objects.first()
usuario = Usuario.objects.filter(empresa=empresa).first()

if not empresa or not usuario:
    print("ERROR: No hay empresa o usuario. Ejecuta primero crear_datos_demo.py")
    exit()

print(f"Empresa: {empresa.nombre}")
print(f"Usuario: {usuario.username}")

# ─── ACTIVOS DEL CLIENTE ─────────────────────────────────
print("\n=== Creando Activos del Cliente ===")

activos_data = [
    {
        'codigo_equipo': 'BOM-AC-001',
        'nombre': 'Bomba centrífuga agua caliente',
        'tipo': 'BOMBA',
        'marca': 'Grundfos',
        'modelo': 'CR 32-2',
        'serial': 'GF-2024-7891',
        'ubicacion': 'Hotel Meliá Caracas',
        'area': 'Sala de calderas - Nivel Sótano',
        'cliente_nombre': 'Hotel Meliá Caracas',
        'cliente_rif': 'J-00123456-7',
        'estado': 'EN_REPARACION',
        'fecha_instalacion': datetime.date(2019, 6, 15),
        'frecuencia_mtto_dias': 180,
        'proximo_mtto': datetime.date(2026, 6, 15),
        'especificaciones': 'Caudal: 32 m³/h\nPresión: 20 bar\nTemperatura máx: 120°C\nPotencia motor: 7.5 kW\nMaterial carcasa: Acero inoxidable AISI 304',
    },
    {
        'codigo_equipo': 'CAL-001',
        'nombre': 'Calderín vapor horizontal',
        'tipo': 'CALDERIN',
        'marca': 'Cleaver-Brooks',
        'modelo': 'CB-200',
        'serial': 'CB-2018-4523',
        'ubicacion': 'Produsal C.A. - Planta Barquisimeto',
        'area': 'Sala de calderas',
        'cliente_nombre': 'Produsal C.A.',
        'cliente_rif': 'J-30198765-4',
        'estado': 'OPERATIVO',
        'fecha_instalacion': datetime.date(2018, 3, 10),
        'frecuencia_mtto_dias': 365,
        'proximo_mtto': datetime.date(2026, 3, 10),
        'especificaciones': 'Capacidad: 200 BHP\nPresión de trabajo: 150 PSI\nCombustible: Gas natural\nSuperficie calefacción: 200 ft²',
    },
    {
        'codigo_equipo': 'TQ-AI-001',
        'nombre': 'Tanque almacenamiento acero inoxidable',
        'tipo': 'TANQUE',
        'marca': 'ITBCA (fabricación propia)',
        'modelo': 'TQ-5000L-SS304',
        'serial': 'ITBCA-2022-0015',
        'ubicacion': 'Produsal C.A. - Planta Barquisimeto',
        'area': 'Área de proceso',
        'cliente_nombre': 'Produsal C.A.',
        'cliente_rif': 'J-30198765-4',
        'estado': 'OPERATIVO',
        'fecha_instalacion': datetime.date(2022, 9, 20),
        'frecuencia_mtto_dias': 730,
        'proximo_mtto': datetime.date(2026, 9, 20),
        'especificaciones': 'Capacidad: 5,000 L\nMaterial: AISI 304\nEspesor: 3mm\nAcabado interior: Pulido sanitario\nConexiones: Tri-clamp 2"',
    },
    {
        'codigo_equipo': 'IC-001',
        'nombre': 'Intercambiador de calor de placas',
        'tipo': 'INTERCAMBIADOR',
        'marca': 'Alfa Laval',
        'modelo': 'M10-BFG',
        'serial': 'AL-2021-8876',
        'ubicacion': 'Hotel Meliá Caracas',
        'area': 'Sala de máquinas - Piso técnico',
        'cliente_nombre': 'Hotel Meliá Caracas',
        'cliente_rif': 'J-00123456-7',
        'estado': 'OPERATIVO',
        'fecha_instalacion': datetime.date(2021, 1, 8),
        'frecuencia_mtto_dias': 365,
        'proximo_mtto': datetime.date(2026, 1, 8),
        'especificaciones': 'Tipo: Placas\nCapacidad: 500 kW\nFluido primario: Agua caliente\nFluido secundario: Agua de piscina\nMaterial placas: AISI 316',
        'notas': 'Requiere cambio de empaques en próximo mantenimiento',
    },
    {
        'codigo_equipo': 'CAN-001',
        'nombre': 'Canoa autolimpiante para evaporador',
        'tipo': 'ESTRUCTURA',
        'marca': 'ITBCA (fabricación propia)',
        'modelo': 'CAN-AL-3M',
        'serial': '',
        'ubicacion': 'Produsal C.A. - Planta Barquisimeto',
        'area': 'Línea de evaporación',
        'cliente_nombre': 'Produsal C.A.',
        'cliente_rif': 'J-30198765-4',
        'estado': 'OPERATIVO',
        'fecha_instalacion': None,
        'frecuencia_mtto_dias': None,
        'proximo_mtto': None,
        'especificaciones': 'Longitud: 3 m\nAncho: 0.6 m\nMaterial: Acero inoxidable AISI 304\nSistema de limpieza: Automático por aspersores',
        'notas': 'Cotización COT-2026-2865 en borrador',
    },
]

for data in activos_data:
    obj, created = ActivoCliente.objects.get_or_create(
        empresa=empresa,
        codigo_equipo=data['codigo_equipo'],
        defaults={**data, 'creado_por': usuario},
    )
    status = "CREADO" if created else "ya existe"
    print(f"  {data['codigo_equipo']}: {data['nombre']} — {status}")


# ─── CARGOS DE NÓMINA ─────────────────────────────────
print("\n=== Creando Cargos de Nómina ===")

cargos_data = [
    {'codigo': 'SOL-6G', 'nombre': 'Soldador certificado 6G', 'nivel': 'ESPECIALISTA', 'costo_hora': Decimal('18.00')},
    {'codigo': 'SOL-3G', 'nombre': 'Soldador 3G', 'nivel': 'OFICIAL', 'costo_hora': Decimal('14.00')},
    {'codigo': 'TUB-01', 'nombre': 'Tubero/Montador', 'nivel': 'OFICIAL', 'costo_hora': Decimal('12.00')},
    {'codigo': 'MEC-01', 'nombre': 'Mecánico industrial', 'nivel': 'OFICIAL', 'costo_hora': Decimal('13.00')},
    {'codigo': 'AYU-01', 'nombre': 'Ayudante de taller', 'nivel': 'AYUDANTE', 'costo_hora': Decimal('7.00')},
    {'codigo': 'SUP-01', 'nombre': 'Supervisor de obra', 'nivel': 'SUPERVISOR', 'costo_hora': Decimal('22.00')},
    {'codigo': 'ING-01', 'nombre': 'Ingeniero de proyecto', 'nivel': 'INGENIERO', 'costo_hora': Decimal('28.00')},
    {'codigo': 'PUL-01', 'nombre': 'Pulidor/Acabado', 'nivel': 'MAESTRO', 'costo_hora': Decimal('15.00')},
    {'codigo': 'CAL-01', 'nombre': 'Calderero', 'nivel': 'MAESTRO', 'costo_hora': Decimal('16.00')},
    {'codigo': 'PIN-01', 'nombre': 'Pintor industrial', 'nivel': 'OFICIAL', 'costo_hora': Decimal('10.00')},
]

for data in cargos_data:
    obj, created = CargoTrabajador.objects.get_or_create(
        empresa=empresa,
        codigo=data['codigo'],
        defaults=data,
    )
    status = "CREADO" if created else "ya existe"
    print(f"  {data['codigo']}: {data['nombre']} (${data['costo_hora']}/h) — {status}")


# ─── Vincular activos a cotizaciones existentes ──────────
print("\n=== Vinculando activos a cotizaciones ===")
from apps.cotizaciones.models import Cotizacion

# Bomba agua caliente → COT que contiene "bomba"
try:
    cot_bomba = Cotizacion.objects.filter(empresa=empresa, nombre_proyecto__icontains='bomba').first()
    if cot_bomba:
        activo_bomba = ActivoCliente.objects.get(empresa=empresa, codigo_equipo='BOM-AC-001')
        cot_bomba.activo_cliente = activo_bomba
        cot_bomba.save(update_fields=['activo_cliente'])
        print(f"  {cot_bomba.numero} → {activo_bomba.codigo_equipo}")
except Exception as e:
    print(f"  Error vinculando bomba: {e}")

# Canoa → COT que contiene "canoa"
try:
    cot_canoa = Cotizacion.objects.filter(empresa=empresa, nombre_proyecto__icontains='canoa').first()
    if cot_canoa:
        activo_canoa = ActivoCliente.objects.get(empresa=empresa, codigo_equipo='CAN-001')
        cot_canoa.activo_cliente = activo_canoa
        cot_canoa.save(update_fields=['activo_cliente'])
        print(f"  {cot_canoa.numero} → {activo_canoa.codigo_equipo}")
except Exception as e:
    print(f"  Error vinculando canoa: {e}")

# Calderín → COT que contiene "calderín" o "calderin"
try:
    cot_cal = Cotizacion.objects.filter(empresa=empresa, nombre_proyecto__icontains='calder').first()
    if cot_cal:
        activo_cal = ActivoCliente.objects.get(empresa=empresa, codigo_equipo='CAL-001')
        cot_cal.activo_cliente = activo_cal
        cot_cal.save(update_fields=['activo_cliente'])
        print(f"  {cot_cal.numero} → {activo_cal.codigo_equipo}")
except Exception as e:
    print(f"  Error vinculando calderín: {e}")

# Vincular proyecto existente con activo
print("\n=== Vinculando activos a proyectos ===")
from apps.proyectos.models import Proyecto
try:
    proy = Proyecto.objects.filter(empresa=empresa).first()
    if proy and proy.cotizacion_origen and proy.cotizacion_origen.activo_cliente:
        proy.activo_cliente = proy.cotizacion_origen.activo_cliente
        proy.save(update_fields=['activo_cliente'])
        print(f"  {proy.codigo} → {proy.activo_cliente.codigo_equipo}")
except Exception as e:
    print(f"  Error vinculando proyecto: {e}")

print("\n✓ Datos demo de Activos y Nómina creados correctamente.")
