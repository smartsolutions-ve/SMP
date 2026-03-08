"""
Script para crear datos demo basados en los presupuestos reales de I.T.B.C.A.
Ejecutar con: python manage.py shell < scripts/crear_datos_demo.py
O desde manage.py con USE_SQLITE=true python manage.py shell -c "exec(open('scripts/crear_datos_demo.py').read())"
"""
import os
import sys
import django

# Configurar Django si se ejecuta directamente
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    os.environ['USE_SQLITE'] = 'true'
    django.setup()

from decimal import Decimal
import datetime
from apps.core.models import Empresa, Usuario
from apps.bd_costos.models import CategoriaItem, ItemCosto, HistorialPrecio
from apps.cotizaciones.models import Cotizacion, PartidaCotizacion
from apps.proyectos.models import Proyecto, PartidaProyecto, RegistroAvance

empresa = Empresa.objects.get(rif='J-30803985-3')
usuario = Usuario.objects.get(username='valmore')

print(f"Creando datos demo para: {empresa.nombre}")
print("=" * 60)

# ====================================================
# CATEGORÍAS
# ====================================================
cats_data = [
    ('01', 'SERVICIOS MECÁNICOS', None),
    ('02', 'FABRICACIÓN METÁLICA', None),
    ('03', 'SUMINISTROS', None),
    ('04', 'MANO DE OBRA', None),
    ('01.01', 'Mantenimiento de Bombas', '01'),
    ('01.02', 'Mantenimiento de Calderas', '01'),
    ('02.01', 'Fabricación Acero Inoxidable', '02'),
    ('02.02', 'Montaje y Soldadura', '02'),
    ('03.01', 'Materiales Mecánicos', '03'),
    ('03.02', 'Accesorios y Tuberías', '03'),
    ('04.01', 'Técnicos Especializados', '04'),
    ('04.02', 'Ayudantes', '04'),
]

cats = {}
for codigo, nombre, padre_codigo in cats_data:
    padre = cats.get(padre_codigo) if padre_codigo else None
    cat, _ = CategoriaItem.objects.get_or_create(
        empresa=empresa, codigo=codigo,
        defaults={'nombre': nombre, 'padre': padre}
    )
    cats[codigo] = cat
    print(f"  Categoría: {codigo} - {nombre}")

# ====================================================
# ÍTEMS DE COSTO (reales del cliente)
# ====================================================
items_data = [
    # Materiales mecánicos
    ('ROD-001', 'Rodamiento sellado 6205-2RS', ItemCosto.TIPO_MATERIAL, '03.01', 'un', Decimal('12.50')),
    ('ROD-002', 'Rodamiento sellado 6206-2RS', ItemCosto.TIPO_MATERIAL, '03.01', 'un', Decimal('15.00')),
    ('SEL-001', 'Sello mecánico para bomba 1"', ItemCosto.TIPO_MATERIAL, '03.01', 'un', Decimal('25.00')),
    ('SEL-002', 'Sello mecánico para bomba 1.5"', ItemCosto.TIPO_MATERIAL, '03.01', 'un', Decimal('35.00')),
    ('TUB-001', 'Tubería acero inoxidable 304 1"', ItemCosto.TIPO_MATERIAL, '03.02', 'ml', Decimal('18.00')),
    ('TUB-002', 'Tubería acero inoxidable 304 2"', ItemCosto.TIPO_MATERIAL, '03.02', 'ml', Decimal('32.00')),
    ('VAL-001', 'Válvula de bola inox 1"', ItemCosto.TIPO_MATERIAL, '03.02', 'un', Decimal('45.00')),
    ('VAL-002', 'Válvula toma muestra 1" acero inox', ItemCosto.TIPO_MATERIAL, '03.02', 'un', Decimal('120.00')),
    ('LAM-001', 'Lámina acero inoxidable 304 1/8"', ItemCosto.TIPO_MATERIAL, '02.01', 'kg', Decimal('8.50')),
    ('LAM-002', 'Lámina acero inoxidable 304 3/16"', ItemCosto.TIPO_MATERIAL, '02.01', 'kg', Decimal('9.20')),
    ('ELE-001', 'Electrodo inoxidable E308L-16 3/32"', ItemCosto.TIPO_MATERIAL, '02.02', 'kg', Decimal('22.00')),
    # Mano de obra
    ('MO-SOL', 'Soldador TIG acero inoxidable', ItemCosto.TIPO_MANO_OBRA, '04.01', 'dia', Decimal('85.00')),
    ('MO-MEC', 'Mecánico industrial especialista', ItemCosto.TIPO_MANO_OBRA, '04.01', 'dia', Decimal('75.00')),
    ('MO-AYU', 'Ayudante mecánico', ItemCosto.TIPO_MANO_OBRA, '04.02', 'dia', Decimal('35.00')),
    ('MO-SUP', 'Supervisor de obra', ItemCosto.TIPO_MANO_OBRA, '04.01', 'dia', Decimal('95.00')),
    # Equipos
    ('EQ-SOL', 'Alquiler equipo soldadura TIG', ItemCosto.TIPO_EQUIPO, None, 'dia', Decimal('30.00')),
    ('EQ-MEC', 'Alquiler torno mecánico', ItemCosto.TIPO_EQUIPO, None, 'hora', Decimal('25.00')),
    # Subcontratos
    ('SC-TRNSP', 'Transporte y flete', ItemCosto.TIPO_SUBCONTRATO, None, 'lote', Decimal('150.00')),
]

items_created = {}
for codigo, descripcion, tipo, cat_codigo, unidad, precio in items_data:
    cat = cats.get(cat_codigo) if cat_codigo else None
    item, _ = ItemCosto.objects.get_or_create(
        empresa=empresa, codigo=codigo,
        defaults={
            'descripcion': descripcion,
            'tipo': tipo,
            'categoria': cat,
            'unidad': unidad,
            'precio_actual': precio,
            'moneda': 'USD',
            'creado_por': usuario,
        }
    )
    # Historial inicial
    if not HistorialPrecio.objects.filter(item=item).exists():
        HistorialPrecio.objects.create(
            item=item, precio=precio, moneda='USD',
            observacion='Precio inicial', usuario=usuario
        )
    items_created[codigo] = item

print(f"  {len(items_data)} ítems de costo creados")

# ====================================================
# COTIZACIONES REALES (de los Excel compartidos)
# ====================================================

# Cotización 2836 - Reparación bomba agua caliente
cot_2836, created = Cotizacion.objects.get_or_create(
    numero='COT-2025-2836',
    defaults={
        'empresa': empresa,
        'cliente_nombre': 'Plata Catia La Mar',
        'cliente_direccion': 'Catia La Mar, Vargas',
        'nombre_proyecto': 'Reparación y Mantenimiento de Bomba Agua Caliente en Calderas',
        'descripcion': 'Desmontaje, cambio de rodamientos y sellos, montaje de bomba en caldera agua caliente.',
        'ubicacion': 'Plata Catia La Mar, Vargas',
        'fecha_vencimiento': datetime.date(2025, 2, 17),
        'margen_utilidad_porcentaje': Decimal('15.00'),
        'estado': Cotizacion.ESTADO_APROBADA,
        'creado_por': usuario,
        'terminos_condiciones': empresa.terminos_condiciones_default,
        'subtotal': Decimal('5735.26'),
        'utilidad_monto': Decimal('860.29'),
        'total': Decimal('6595.54'),
    }
)
if created:
    PartidaCotizacion.objects.create(
        cotizacion=cot_2836, orden=0,
        codigo='01.01',
        descripcion='Desmontaje y Mantenimiento a Bombas de Circulación en Caldera',
        categoria='SERVICIOS MECÁNICOS',
        unidad='UNID',
        cantidad=Decimal('2'),
        precio_unitario=Decimal('2867.63'),
        subtotal=Decimal('5735.26'),
    )
    print("  Cotización 2836 creada")

# Cotización 2864 - Toma muestra calderín
cot_2864, created = Cotizacion.objects.get_or_create(
    numero='COT-2026-2864',
    defaults={
        'empresa': empresa,
        'cliente_nombre': 'Plata Catia La Mar',
        'cliente_contacto': 'Samuel Cárdenas',
        'cliente_direccion': 'Catia La Mar, Vargas',
        'nombre_proyecto': 'Suministro e Instalación de Toma Muestra en Calderín 1 y 2',
        'descripcion': 'Suministro e instalación de toma muestra 1" en calderín 1 y 2.',
        'ubicacion': 'Plata Catia La Mar, Vargas',
        'fecha_vencimiento': datetime.date(2026, 3, 17),
        'margen_utilidad_porcentaje': Decimal('15.00'),
        'estado': Cotizacion.ESTADO_ENVIADA,
        'creado_por': usuario,
        'terminos_condiciones': empresa.terminos_condiciones_default,
        'subtotal': Decimal('656.30'),
        'utilidad_monto': Decimal('98.45'),
        'total': Decimal('754.75'),
    }
)
if created:
    PartidaCotizacion.objects.create(
        cotizacion=cot_2864, orden=0,
        codigo='01.01',
        descripcion='Suministro e instalación de toma muestra 1" en calderín 1 y 2',
        categoria='SUMINISTROS',
        unidad='unid',
        cantidad=Decimal('2'),
        precio_unitario=Decimal('328.15'),
        subtotal=Decimal('656.30'),
    )
    print("  Cotización 2864 creada")

# Cotización 2865 - Canoa autolimpiante
cot_2865, created = Cotizacion.objects.get_or_create(
    numero='COT-2026-2865',
    defaults={
        'empresa': empresa,
        'cliente_nombre': 'Produsal',
        'cliente_direccion': 'Valencia, Carabobo',
        'nombre_proyecto': 'Suministro y Fabricación de Canoa Autolimpiante para Sin Fin #1 Ensacado',
        'descripcion': 'Fabricación de canoa autolimpiante para tornillo sin fin #1 del área de ensacado.',
        'ubicacion': 'Produsal — Valencia, Carabobo',
        'fecha_vencimiento': datetime.date(2026, 3, 20),
        'margen_utilidad_porcentaje': Decimal('15.00'),
        'estado': Cotizacion.ESTADO_BORRADOR,
        'creado_por': usuario,
        'terminos_condiciones': empresa.terminos_condiciones_default,
        'subtotal': Decimal('12019.37'),
        'utilidad_monto': Decimal('1802.91'),
        'total': Decimal('13822.28'),
    }
)
if created:
    PartidaCotizacion.objects.create(
        cotizacion=cot_2865, orden=0,
        codigo='01.01',
        descripcion='Fabricación de canoa autolimpiante para Sin Fin #1 — Acero Inoxidable 304',
        categoria='FABRICACIÓN METÁLICA',
        unidad='ML',
        cantidad=Decimal('6.85'),
        precio_unitario=Decimal('1754.65'),
        subtotal=Decimal('12019.37'),
    )
    print("  Cotización 2865 creada")

# ====================================================
# PROYECTO EN EJECUCIÓN (de cotización 2836)
# ====================================================
if not Proyecto.objects.filter(cotizacion_origen=cot_2836).exists():
    proyecto = Proyecto.objects.create(
        empresa=empresa,
        cotizacion_origen=cot_2836,
        nombre='Reparación Bomba Agua Caliente Calderas — Plata Catia La Mar',
        descripcion=cot_2836.descripcion,
        ubicacion='Plata Catia La Mar, Vargas',
        cliente_nombre='Plata Catia La Mar',
        fecha_inicio_planeada=datetime.date(2026, 2, 10),
        fecha_inicio_real=datetime.date(2026, 2, 12),
        fecha_fin_planeada=datetime.date(2026, 2, 28),
        valor_contrato=cot_2836.total,
        moneda='USD',
        estado=Proyecto.ESTADO_EN_EJECUCION,
        gerente_proyecto=usuario,
        creado_por=usuario,
        porcentaje_avance=Decimal('65.00'),
    )
    # Partidas del proyecto
    p1 = PartidaProyecto.objects.create(
        proyecto=proyecto, orden=0,
        codigo='01.01',
        descripcion='Desmontaje y Mantenimiento Bomba de Circulación #1',
        categoria='SERVICIOS MECÁNICOS',
        unidad='UNID',
        cantidad_presupuestada=Decimal('1'),
        precio_unitario_presupuestado=Decimal('2867.63'),
        costo_presupuestado=Decimal('2867.63'),
        cantidad_ejecutada=Decimal('1'),
        costo_real=Decimal('2750.00'),
        estado=PartidaProyecto.ESTADO_COMPLETADA,
        porcentaje_avance=Decimal('100.00'),
    )
    p2 = PartidaProyecto.objects.create(
        proyecto=proyecto, orden=1,
        codigo='01.02',
        descripcion='Desmontaje y Mantenimiento Bomba de Circulación #2',
        categoria='SERVICIOS MECÁNICOS',
        unidad='UNID',
        cantidad_presupuestada=Decimal('1'),
        precio_unitario_presupuestado=Decimal('2867.63'),
        costo_presupuestado=Decimal('2867.63'),
        cantidad_ejecutada=Decimal('0.30'),
        costo_real=Decimal('850.00'),
        estado=PartidaProyecto.ESTADO_EN_PROCESO,
        porcentaje_avance=Decimal('30.00'),
    )

    # Registros de avance
    RegistroAvance.objects.create(
        partida=p1,
        fecha=datetime.date(2026, 2, 12),
        cantidad_ejecutada_dia=Decimal('0.5'),
        costo_dia=Decimal('1200.00'),
        observaciones='Desmontaje bomba #1 completado. Rodamientos y sellos en mal estado.',
        registrado_por=usuario,
    )
    RegistroAvance.objects.create(
        partida=p1,
        fecha=datetime.date(2026, 2, 14),
        cantidad_ejecutada_dia=Decimal('0.5'),
        costo_dia=Decimal('1550.00'),
        observaciones='Instalación rodamientos nuevos 6205-2RS y sellos mecánicos. Prueba de funcionamiento OK.',
        registrado_por=usuario,
    )
    RegistroAvance.objects.create(
        partida=p2,
        fecha=datetime.date(2026, 2, 15),
        cantidad_ejecutada_dia=Decimal('0.3'),
        costo_dia=Decimal('850.00'),
        observaciones='Inicio desmontaje bomba #2. Problema de acceso por espacio reducido.',
        registrado_por=usuario,
    )

    print(f"  Proyecto en ejecución creado: {proyecto.codigo}")

print("\n" + "=" * 60)
print("✅ Datos demo creados exitosamente.")
print("   Usuario: valmore | Contraseña: itbca2026")
print("   URL: http://127.0.0.1:8080/auth/login/")
print("=" * 60)
