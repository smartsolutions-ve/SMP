# Arquitectura Multi-tenant — Decisiones y Estrategia

**Proyecto:** Smart Project Management — SmartSolutions VE
**Fecha:** 2026-03-07
**Autor:** Simón Briceño

---

## Indice

1. [Que es multi-tenant y que tenemos ahora](#1-que-es-multi-tenant)
2. [Multi-tenant vs instancia por cliente](#2-comparativa)
3. [Por que multi-tenant es la decision correcta](#3-decision)
4. [Riesgos y como mitigarlos](#4-riesgos)
5. [Como manejar personalizaciones por cliente](#5-personalizaciones)
6. [Estrategia de crecimiento por fases](#6-fases)
7. [Checklist antes de agregar un nuevo cliente](#7-checklist)

---

## 1. Que es multi-tenant

Un sistema multi-tenant es aquel donde **multiples clientes (tenants) comparten la misma instalacion del software** pero cada uno ve exclusivamente sus propios datos.

Existen tres niveles de aislamiento, de menor a mayor:

```
NIVEL 1 — Schema compartido (lo que tenemos ahora)
┌─────────────────────────────────────┐
│           PostgreSQL DB             │
│  ┌──────────────────────────────┐   │
│  │  Tabla proyectos             │   │
│  │  empresa_id=1 → Valmore      │   │
│  │  empresa_id=2 → Cliente B    │   │
│  │  empresa_id=3 → Cliente C    │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
  Aislamiento: lógico (por filtro SQL)
  Complejidad: baja
  Costo: bajo


NIVEL 2 — Schema separado por tenant
┌─────────────────────────────────────┐
│           PostgreSQL DB             │
│  schema_valmore.proyectos           │
│  schema_clienteb.proyectos          │
│  schema_clientec.proyectos          │
└─────────────────────────────────────┘
  Aislamiento: medio (schemas separados)
  Complejidad: media
  Costo: medio


NIVEL 3 — Base de datos separada
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  DB Valmore  │ │  DB Cliente B│ │  DB Cliente C│
└──────────────┘ └──────────────┘ └──────────────┘
  Aislamiento: total
  Complejidad: alta
  Costo: alto (una VPS por cliente)
```

**El sistema actual usa Nivel 1.** Todas las entidades tienen FK a `Empresa` y el `TenantMiddleware` se encarga de filtrar.

---

## 2. Comparativa: Multi-tenant vs Instancia por cliente

### Multi-tenant (una sola instalacion)

| Aspecto | Detalle |
|---------|---------|
| Infraestructura | 1 servidor para N clientes |
| Costo operativo | $20-40/mes independiente de cuantos clientes haya |
| Actualizaciones | Despliegas una vez, todos los clientes la reciben |
| Customizacion | Limitada — los cambios afectan a todos |
| Aislamiento de datos | Logico (filtros SQL) |
| Administracion | Un solo entorno que mantener |
| Escalabilidad | Alta — puedes agregar 50 clientes sin nueva infraestructura |
| Riesgo de contaminacion | Existe si hay bugs en los filtros |

### Instancia por cliente (un servidor por cliente)

| Aspecto | Detalle |
|---------|---------|
| Infraestructura | 1 servidor por cliente |
| Costo operativo | $10-20/mes por cliente (se come tu margen) |
| Actualizaciones | Debes actualizar cada instalacion manualmente o con scripts |
| Customizacion | Total — cada cliente puede tener su propia version |
| Aislamiento de datos | Total — bases de datos fisicamente separadas |
| Administracion | N entornos, N dominios, N SSL, N backups |
| Escalabilidad | Baja — crece en complejidad operativa con cada cliente |
| Riesgo de contaminacion | Ninguno |

### Cuando usar cada uno

| Condicion del cliente | Recomendacion |
|-----------------------|---------------|
| PYME, $100-120/mes | Multi-tenant |
| Requiere SLA formal con uptime garantizado | Instancia propia |
| Paga $500+/mes | Instancia propia (el margen lo permite) |
| Pide auditorias de seguridad / ISO | Instancia propia o Nivel 3 |
| Sector salud, gobierno, banca | Instancia propia obligatorio |
| Logica de negocio identica a otros clientes | Multi-tenant |
| Necesita integraciones especificas con sus sistemas internos | Evaluar caso |

**Para el mercado actual de SmartSolutions VE (PYMEs contratistas venezolanas): multi-tenant es la decision correcta.**

---

## 3. Por que multi-tenant es la decision correcta

### El modelo de negocio lo exige

Con $100/mes de suscripcion y una VPS de $20/mes compartida entre 10 clientes:

```
Ingresos:  10 clientes × $100 = $1,000/mes
Servidor:  $20/mes
Margen:    $980/mes (98%)
```

Con instancias separadas y 10 clientes:

```
Ingresos:  10 clientes × $100 = $1,000/mes
Servidores: 10 × $15 = $150/mes
Tiempo DevOps: ~10 horas/mes × $20/hora = $200/mes
Margen:    $650/mes (65%) y decreciendo con cada cliente
```

A 20 clientes con instancias separadas, el tiempo de administracion se vuelve un trabajo de tiempo completo.

### El modelo de datos ya es suficientemente generico

El sistema cubre cualquier tipo de contratista porque:

- `CategoriaItem` y `ItemCosto` son configurables por empresa — cada cliente define su propio catalogo de costos
- `PartidaCotizacion` y `PartidaProyecto` funcionan igual para metalmecánica, civil, HVAC o cualquier especialidad
- Las unidades de medida son flexibles (m2, ml, kg, hora, dia, lote, etc.)
- Los flujos de cotizacion y proyecto son universales en el sector construccion/contratistas

```
Valmore (acero inoxidable):
  CategoriaItem: "Acero Inoxidable" > "Tuberia" > "304"
  ItemCosto: [TUB-304-1", kg, $8.50/kg]

Cliente B (construccion civil):
  CategoriaItem: "Concreto" > "Estructural"
  ItemCosto: [CONC-3000PSI, m3, $180/m3]

Cliente C (electricidad):
  CategoriaItem: "Cableado" > "Baja Tension"
  ItemCosto: [CAB-12AWG, ml, $2.10/ml]

→ Los tres usan el mismo sistema sin conflicto
```

---

## 4. Riesgos y como mitigarlos

### Riesgo 1 — Fuga de datos entre tenants (el mas critico)

**Que puede pasar:** Un bug en una vista que olvide filtrar por `empresa` devuelve datos de otro cliente.

**Como prevenirlo:**

Regla de oro: **toda query que toque datos de negocio debe incluir `empresa=request.tenant`**.

```python
# MAL — nunca hagas esto en una vista
proyectos = Proyecto.objects.filter(estado='EN_EJECUCION')

# BIEN — siempre filtra por tenant
proyectos = Proyecto.objects.filter(empresa=request.tenant, estado='EN_EJECUCION')
```

**Test de seguridad a agregar** (antes de agregar el segundo cliente real):

```python
# apps/core/tests.py
class TenantIsolationTest(TestCase):
    def test_empresa_a_no_ve_datos_de_empresa_b(self):
        empresa_a = Empresa.objects.create(nombre="A", rif="J-00000001-0")
        empresa_b = Empresa.objects.create(nombre="B", rif="J-00000002-0")
        Proyecto.objects.create(empresa=empresa_a, ...)
        Proyecto.objects.create(empresa=empresa_b, ...)

        # Simular usuario de empresa A
        self.client.force_login(usuario_empresa_a)
        response = self.client.get('/proyectos/')
        proyectos_vistos = response.context['proyectos']

        # Solo debe ver los de su empresa
        self.assertTrue(all(p.empresa == empresa_a for p in proyectos_vistos))
```

### Riesgo 2 — Performance con muchos clientes

**Que puede pasar:** Con 50 empresas y 500 proyectos en la misma tabla, las queries se vuelven lentas.

**Como prevenirlo:**

Los indices ya existen en el modelo (`empresa, estado`). Cuando superes 20 clientes activos, agrega:

```python
# En cada modelo principal, asegurar que empresa este indexado
class Meta:
    indexes = [
        models.Index(fields=['empresa', 'estado']),
        models.Index(fields=['empresa', '-fecha_creacion']),  # para listas ordenadas
    ]
```

### Riesgo 3 — Un cliente afecta a otros (recursos compartidos)

**Que puede pasar:** Un cliente sube 500 fotos de alta resolucion y llena el disco que comparten todos.

**Como prevenirlo:**

```python
# apps/proyectos/views.py — ya existe limite de 5MB por foto
# Agregar: limite de almacenamiento total por empresa (pendiente)
# Solucion futura: mover media a S3/DigitalOcean Spaces con paths por empresa
MEDIA_ROOT / 'empresas' / str(empresa.id) / 'fotos' /
```

---

## 5. Como manejar personalizaciones por cliente

Este es el tema mas delicado. Hay cinco niveles de personalizacion, de menor a mayor impacto:

---

### Nivel A — Personalizacion de datos (ya soportado)

Cada cliente configura su propio catalogo sin tocar codigo.

**Ejemplos:**
- Sus propias categorias de costos
- Sus propios terminos y condiciones default
- Su logo y nombre comercial en PDFs
- Su moneda preferida (USD/VES)
- Su margen de utilidad por defecto

**Como funciona:** Todo esto ya esta en el modelo `Empresa`. No requiere nada adicional.

---

### Nivel B — Personalizacion de configuracion por empresa

Algunas opciones de comportamiento que cada empresa puede activar/desactivar.

**Ejemplos:**
- Mostrar o no el costo real a supervisores
- Requerir aprobacion de orden de cambio o hacerla automatica
- Permitir fechas de avance futuras o solo pasadas
- Habilitar o no el modulo de reportes al cliente

**Como implementarlo:**

```python
# Agregar a apps/core/models.py en el modelo Empresa
class Empresa(models.Model):
    # ... campos actuales ...

    # Configuracion de comportamiento
    requiere_aprobacion_oc = models.BooleanField(
        'Requiere aprobacion para Ordenes de Cambio', default=True
    )
    permite_fechas_avance_futuras = models.BooleanField(
        'Permitir registrar avances en fechas futuras', default=False
    )
    mostrar_costos_a_supervisor = models.BooleanField(
        'Supervisores pueden ver costos presupuestados', default=False
    )
    dias_alerta_cotizacion_sin_seguimiento = models.PositiveSmallIntegerField(
        'Dias sin seguimiento para alerta', default=5
    )
```

En las vistas:

```python
# En lugar de logica fija
if request.user.rol == 'SUPERVISOR':
    # no mostrar costos

# Con configuracion por empresa
if request.user.rol == 'SUPERVISOR' and not request.tenant.mostrar_costos_a_supervisor:
    # no mostrar costos
```

---

### Nivel C — Campos adicionales por empresa

Un cliente necesita registrar informacion que otros no necesitan.

**Ejemplos:**
- Valmore necesita registrar el "numero de certificado de calidad" en cada partida
- Otro cliente necesita un campo "numero de contrato SENIAT" en cotizaciones
- Otro necesita registrar "zona geografica" en proyectos

**Estrategia: campos opcionales en el modelo base**

Antes de crear campos especificos por cliente, evalua si el campo puede ser util para otros:

```python
# Si es potencialmente util para varios clientes → agrega al modelo
class Proyecto(models.Model):
    referencia_externa = models.CharField(
        'Referencia externa / N° contrato cliente',
        max_length=100, blank=True
    )
    # blank=True lo hace opcional — quien no lo necesite lo ignora
```

**Estrategia: modelo de metadatos clave-valor (para casos muy especificos)**

Si el campo es muy especifico y solo un cliente lo necesita:

```python
# apps/core/models.py — agregar cuando sea necesario
class MetadatoEmpresa(models.Model):
    """
    Campos personalizados que una empresa especifica necesita
    en sus entidades. Evita alterar los modelos principales.
    """
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    entidad = models.CharField(max_length=50)  # 'proyecto', 'cotizacion', etc.
    entidad_id = models.UUIDField()
    clave = models.CharField(max_length=100)
    valor = models.TextField()

    class Meta:
        unique_together = [('empresa', 'entidad', 'entidad_id', 'clave')]
```

Uso:

```python
# Guardar dato especifico de Valmore en un proyecto
MetadatoEmpresa.objects.create(
    empresa=valmore,
    entidad='proyecto',
    entidad_id=proyecto.id,
    clave='certificado_calidad',
    valor='CERT-2026-0042'
)
```

Este enfoque es poderoso pero tiene el costo de que los metadatos no son consultables facilmente en SQL. Usarlo solo cuando el campo es realmente exclusivo de un cliente.

---

### Nivel D — Flujos de negocio distintos

Un cliente necesita que el sistema se comporte diferente en un flujo critico.

**Ejemplos:**
- Valmore: cotizacion → proyecto (flujo normal)
- Cliente B: cotizacion → propuesta tecnica → aprobacion interna → proyecto
- Cliente C: no usa cotizaciones, crea proyectos directamente

**Estrategia: feature flags por empresa**

```python
# apps/core/models.py
class Empresa(models.Model):
    # Modulos habilitados
    modulo_cotizaciones_activo = models.BooleanField(default=True)
    modulo_bd_costos_activo = models.BooleanField(default=True)
    modulo_reportes_activo = models.BooleanField(default=True)

    # Flujos opcionales
    flujo_aprobacion_interna = models.BooleanField(
        'Requiere aprobacion interna antes de enviar cotizacion', default=False
    )
```

En el context processor (`apps/core/context_processors.py`):

```python
def empresa_context(request):
    if request.tenant:
        return {'tenant': request.tenant}
    return {}
```

En templates, para mostrar/ocultar modulos segun el cliente:

```html
{% if tenant.modulo_cotizaciones_activo %}
  <a href="{% url 'cotizaciones_lista' %}">Cotizaciones</a>
{% endif %}
```

---

### Nivel E — Logica completamente diferente (el caso limite)

Un cliente necesita algo tan distinto que no tiene sentido forzarlo en el sistema existente.

**Ejemplo extremo:** Una empresa de consultoria quiere usar el sistema pero su "proyecto" es en realidad una licencia de software con renovaciones anuales, sin partidas fisicas ni avances de obra.

**Estrategia: evaluar si es un producto diferente**

Antes de retorcer el codigo para un cliente, hazte estas preguntas:

1. ¿Este cliente esta pagando suficiente para justificar el desarrollo especifico?
2. ¿Hay al menos 3 clientes potenciales con la misma necesidad?
3. ¿La customizacion rompe la experiencia de los otros clientes?

Si la respuesta a la #3 es si, tienes dos opciones:

**Opcion A — Django apps opcionales por tenant**

Crea la funcionalidad como una app separada que solo se activa para ese cliente:

```
apps/
├── core/
├── cotizaciones/
├── proyectos/
├── ...
└── extensiones/          ← apps opcionales por cliente
    ├── consultoria/      ← solo activa para clientes de consultoria
    ├── inventario/       ← modulo futuro de inventario (Valmore lo quiere)
    └── facturacion/      ← modulo futuro SENIAT
```

```python
# config/settings/base.py
LOCAL_APPS = [
    'apps.core',
    'apps.cotizaciones',
    'apps.proyectos',
    # ...
]

# Las extensiones se activan segun el cliente en la DB
# No en INSTALLED_APPS sino via feature flags
```

**Opcion B — Instancia separada para ese cliente**

Si el cliente necesita el Nivel E y paga bien, es candidato a instancia propia. Eso esta bien — no todos los clientes tienen que ser multi-tenant. Puedes tener:

```
smart-pm.smartsolutions.com     ← instalacion multi-tenant (mayoria)
cliente-especial.smartsolutions.com ← instancia dedicada (cliente premium)
```

---

## 6. Estrategia de crecimiento por fases

### Fase actual (0-5 clientes) — Lo que tenemos

- Multi-tenant Nivel 1 (schema compartido)
- Personalizacion: solo datos (Nivel A)
- Un solo servidor con SQLite o PostgreSQL
- Un solo dominio

```
Prioridad: hacer que el producto funcione bien para Valmore.
No optimizar prematuramente para escala.
```

### Fase 2 (5-20 clientes) — Cuando agregar

- Migrar de SQLite a PostgreSQL si aun no se hizo
- Agregar configuracion por empresa (Nivel B)
- Implementar el test de aislamiento de datos (BUG-8)
- Corregir el race condition de codigos (BUG-1)
- Mover media a DigitalOcean Spaces o S3 (path por empresa)
- Agregar campos opcionales (`referencia_externa`, etc.) segun demanda real

### Fase 3 (20-100 clientes) — Cuando agregar

- Evaluar migracion a schema separado por tenant (Nivel 2) si la performance lo exige
- Sistema de facturacion automatica de suscripciones
- Panel de administracion para gestionar todos los tenants
- Backups automatizados por empresa
- Metricas de uso por cliente

### Fase 4 (100+ clientes) — Futuro

- Infraestructura dedicada por region
- API publica para integraciones de terceros
- Marketplace de extensiones por industria

---

## 7. Checklist antes de agregar un nuevo cliente

Antes de crear el tenant de un nuevo cliente en el sistema, verificar:

### Datos minimos requeridos

- [ ] Razon social completa
- [ ] RIF
- [ ] Email de contacto principal
- [ ] Logo (para cotizaciones y reportes)
- [ ] Moneda que usa (USD / VES / ambas)
- [ ] Margen de utilidad default
- [ ] Terminos y condiciones standard
- [ ] Forma de pago standard

### Configuracion inicial del sistema

- [ ] Crear registro `Empresa` en Django Admin
- [ ] Crear usuario ADMIN del cliente y enviar credenciales
- [ ] Cargar categorias de costos iniciales (puede importar desde Excel)
- [ ] Cargar items de costo frecuentes (al menos 20-30 para que sea util desde el dia 1)
- [ ] Configurar terminos y condiciones en `Empresa.terminos_condiciones_default`
- [ ] Probar login y que el tenant se resuelve correctamente
- [ ] Crear un proyecto demo con datos reales del cliente para la sesion de capacitacion

### Validacion de seguridad

- [ ] Confirmar que el nuevo cliente NO puede ver datos de otros clientes
  ```bash
  # En Django shell
  python manage.py shell
  >>> from apps.proyectos.models import Proyecto
  >>> from apps.core.models import Empresa
  >>> empresa_nueva = Empresa.objects.get(rif='J-XXXXXXXX-X')
  >>> Proyecto.objects.filter(empresa=empresa_nueva).count()  # debe ser 0 o solo los demos
  ```
- [ ] Confirmar que los usuarios del nuevo cliente no tienen `is_superuser=True`
- [ ] Confirmar que la contrasena del admin fue cambiada (no usar la default)

### Capacitacion

- [ ] Sesion 1: Crear cotizacion completa y generar PDF
- [ ] Sesion 2: Convertir cotizacion a proyecto y registrar avances
- [ ] Sesion 3: Ver reportes de rentabilidad
- [ ] Documentar preguntas que surgieron para mejorar el onboarding

---

## Resumen ejecutivo

| Pregunta | Respuesta |
|----------|-----------|
| Multi-tenant o por cliente | Multi-tenant para todos los clientes PYME a $100-120/mes |
| Instancia separada cuando | Cliente paga $500+/mes, exige SLA formal, o necesita logica radicalmente distinta |
| Como manejar diferencias entre clientes | Niveles A→E segun complejidad. Empezar siempre por el nivel mas bajo posible |
| Cuanto puede diferir la logica antes de ser un producto distinto | Cuando los flujos core (cotizacion → proyecto → avance) cambian estructuralmente |
| Que hacer si un cliente necesita algo muy especifico | Feature flags primero, luego app de extension, luego instancia propia como ultimo recurso |
| Riesgo principal de multi-tenant | Fuga de datos entre tenants por query sin filtro. Mitigar con tests de aislamiento |
