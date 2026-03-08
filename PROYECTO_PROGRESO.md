# Smart Project Management — Registro de Progreso

> Actualizado automáticamente a medida que avanza el desarrollo.
> Última actualización: 2026-03-05

---

## 🏢 CLIENTE

| Campo | Valor |
|---|---|
| **Empresa** | Industrias Técnicas Barquisimeto, C.A. |
| **Nombre corto** | I.T.B.C.A. |
| **RIF** | J-30803985-3 |
| **Especialidad** | Montajes y Especialidades en Acero Inoxidable |
| **Dirección** | Calle Guzmán Blanco, Galpón café San Pablo Nro 32-A, Antimano, Caracas |
| **Teléfonos** | 0212-4720427 / 0414-0717668 |
| **Email 1** | industriastecnicasbarquisimeto@gmail.com |
| **Email 2** | ITBCA@HOTMAIL.COM |
| **Años en mercado** | Desde 2001 (23+ años) |
| **Empleados** | 11-20 personas |
| **Contacto principal** | Valmore |

### Equipo de trabajo
- 4 soldadores
- 4 mecánicos
- 2 jefes de seguridad
- 2 supervisores
- 4 ayudantes
- 1 depositario (almacenista)

### Servicios
- Construcción civil y remodelaciones
- Instalaciones eléctricas y mecánicas/HVAC
- Fabricación de piezas y estructuras metálicas (acero inoxidable)
- Mantenimiento industrial y mecánico
- Montaje electromecánico
- Decoraciones

### Volúmenes
- 2-5 proyectos simultáneos
- Duración: 1 semana hasta 3 meses
- Valor por proyecto: $15,000 - $100,000 USD
- 70-89% de proyectos dentro de presupuesto
- Pérdidas estimadas último año por mala estimación: ~$23,000 USD

---

## 🎯 OBJETIVOS DEL SISTEMA

### Empresa desarrolladora
- **SmartSolutions VE** — Valencia, Carabobo, Venezuela
- **Desarrollador:** Simón Briceño | **Socio:** Javier Figueroa
- **Modelo SaaS:** $1,200 implementación + $100-120/mes suscripción

### Objetivos MVP
1. Eliminar dependencia de Excel para cotizaciones y seguimiento
2. Centralizar información de costos, proyectos y clientes
3. Acelerar creación de cotizaciones (de horas a minutos)
4. Visibilidad en tiempo real del avance y rentabilidad
5. Profesionalizar imagen con cotizaciones y reportes de calidad

### Métricas de éxito (3 meses)
- Ahorro % en proyectos por mejor control
- Reducción del tiempo de cotización
- Detectar desviaciones antes de que sea tarde
- Proyectos terminados dentro del presupuesto
- Mejor imagen profesional ante clientes

---

## 🏗️ ARQUITECTURA

### Stack tecnológico
- **Backend:** Django 6.0.3 (Python 3.13)
- **Base de datos:** PostgreSQL 16
- **Frontend:** HTMX + Alpine.js + Tailwind CSS (CDN)
- **Gráficas:** Chart.js
- **PDF:** WeasyPrint o ReportLab
- **Entorno virtual:** `env/` (Python venv)

### Diseño
- Dark glassmorphism (#0F172A fondo, rgba cards)
- Fuentes: Outfit (principal) + JetBrains Mono (números)
- Colores: Azul #0066FF, Verde #22C55E
- Responsive con Tailwind CSS

### Apps Django
```
smart_pm/            ← Proyecto Django raíz
├── config/          ← Settings, URLs raíz, wsgi/asgi
├── apps/
│   ├── core/        ← Empresa (tenant), User, middleware, base views
│   ├── cotizaciones/← Cotizaciones, partidas, PDF
│   ├── bd_costos/   ← ItemCosto, CategoriaItem, HistorialPrecio
│   ├── proyectos/   ← Proyecto, PartidaProyecto, RegistroAvance, Fotos, OC
│   └── reportes/    ← Reportes, KPIs, exportación Excel
├── templates/
├── static/
└── media/
```

### Multi-tenant
- Todas las entidades tienen FK a `Empresa`
- Middleware identifica empresa del usuario autenticado
- Queries filtrados automáticamente por tenant

---

## 📋 MÓDULOS DEL SISTEMA

| # | Módulo | Descripción |
|---|--------|-------------|
| 1 | **Dashboard** | KPIs, proyectos activos, alertas, gráficas |
| 2 | **Cotizaciones** | Crear/editar, partidas, PDF, estados, convertir a proyecto |
| 3 | **BD de Costos** | Items, categorías, historial precios, import/export Excel |
| 4 | **Proyectos** | Ejecución, partidas, registros avance, fotos, órdenes cambio |
| 5 | **Reportes** | Rentabilidad, análisis cotizaciones, costos por categoría |

### Roles de usuario
| Rol | Capacidades |
|-----|-------------|
| ADMIN | Acceso total, gestión usuarios, configuración |
| GERENTE | Cotizaciones, proyectos, BD costos, reportes |
| SUPERVISOR | Registrar avances y fotos (sin ver costos) |
| CLIENTE | Solo ver su cotización/proyecto (solo lectura) |

---

## 📁 EXCELS DEL CLIENTE (Presupuestos reales)

| N° | Trabajo | Cantidad | Precio Unit. | Total |
|----|---------|----------|-------------|-------|
| **2836** | Desmontaje y Mantenimiento Bombas de Circulación (Caldera) | 2 UNID | $3,297.77 | $6,595.54 |
| **2864** | Suministro e instalación toma muestra 1" en Calderín 1 y 2 | 2 unid | $377.37 | $754.75 |
| **2865** | Fabricación Canoa Autolimpiante para Sin Fin #1 (Ensacado Produsal) | 6.85 ML | $2,017.85 | $13,822.28 |

- **Formato Excel:** encabezado empresa + presupuesto numerado + tabla partidas (ÍTEM, DESCRIPCIÓN, UNID, CANT, P.U., TOTAL)
- **Cliente PRODUSAL** mencionado en presupuesto 2865
- **Ubicación obras:** Plata Catia La Mar

---

## 🚀 PROGRESO DEL DESARROLLO

### Estado actual: MVP FUNCIONAL — Post-MVP en desarrollo

| Fase | Estado | Descripción |
|------|--------|-------------|
| ✅ Entorno virtual | Completado | `env/` con Django 6, psycopg2, Pillow, openpyxl, reportlab |
| ✅ Fase 1 | Completado | Estructura Django, modelos completos, migraciones, datos iniciales |
| ✅ Fase 2 | Completado | Templates base glassmorphism, login, dashboard con KPIs |
| ✅ Fase 3 | Completado | BD de Costos — CRUD, categorías, historial precios, API búsqueda |
| ✅ Fase 4 | Completado | Cotizaciones CRUD completo, PDF con ReportLab, convertir a proyecto |
| ✅ Fase 5 | Completado | Proyectos en Ejecución, partidas, avances, fotos, órdenes de cambio |
| ✅ Fase 6 | Completado | Reportes financieros, gráficas Chart.js, datos demo reales cargados |
| ✅ Fase 7 | Completado | Corrección de 8 bugs detectados (modal OC, JSON partidas, x-cloak, etc.) |

---

## 🐛 DEUDA TÉCNICA — Bugs e Issues Identificados

> Revisión de código: 2026-03-07. Estos no son errores visuales sino problemas de arquitectura y rendimiento que deben corregirse antes de agregar más clientes al sistema.

### 🔴 CRÍTICOS — Pueden causar datos corruptos

| # | Archivo | Problema | Impacto | Solución |
|---|---------|----------|---------|----------|
| BUG-1 | `apps/proyectos/models.py:150` | **Race condition en `_generar_codigo()`** — Si dos usuarios crean un proyecto simultáneamente, ambos pueden obtener el mismo código (ej: `PROY-2026-003` duplicado). Mismo problema en `cotizaciones/models.py:131` con `_generar_numero()` | Datos duplicados, falla de constraint | Usar `select_for_update()` dentro de una transacción atómica, o migrar a `AutoField` separado por empresa |
| BUG-2 | `requirements/base.txt:1` | **Discrepancia de versión Django** — requirements dice `Django==6.0.3` pero el servidor corre `5.2.6`. Si alguien reinstala el entorno puede obtener una versión diferente | Inconsistencia entre entornos, bugs impredecibles | Ejecutar `pip show django` y sincronizar `requirements/base.txt` con la versión real instalada |

### 🟡 IMPORTANTES — Afectan rendimiento a escala

| # | Archivo | Problema | Impacto | Solución |
|---|---------|----------|---------|----------|
| BUG-3 | `apps/proyectos/models.py:99` y `apps/proyectos/views.py:26` | **N+1 queries en lista de proyectos** — `costo_real_total` (property) llama `self.partidas.all()` por cada proyecto. 20 proyectos = 21 queries a la DB | Lento con muchos proyectos | Agregar `prefetch_related('partidas')` en `lista_view` |
| BUG-4 | `apps/bd_costos/models.py:41` | **`nombre_jerarquico` sin protección de profundidad** — Property recursiva sin límite real. El comentario dice "máximo 3 niveles" pero el código no lo enforcea | Stack overflow si datos corruptos, queries recursivas | Agregar contador de profundidad o iterar en lugar de recursión |
| BUG-5 | `apps/cotizaciones/models.py:172` | **Recalculo de totales en cada `save()` de partida** — `PartidaCotizacion.save()` llama `cotizacion.calcular_totales()` que hace `self.partidas.all()`. Si importas 50 partidas en bulk, son 50 recalculos | Muy lento en importación masiva desde Excel | Usar `update_fields` + recalcular solo al final en operaciones bulk |

### 🟢 MEJORAS — Calidad de código

| # | Archivo | Problema | Impacto | Solución |
|---|---------|----------|---------|----------|
| BUG-6 | `apps/proyectos/views.py:14`, `apps/cotizaciones/views.py`, `apps/bd_costos/views.py` | **`tenant_required` duplicado en cada app** — El decorador está definido localmente en cada views.py | Difícil de mantener, cambio en uno no afecta los otros | Mover a `apps/core/decorators.py` e importar desde ahí |
| BUG-7 | `config/settings/production.py` | **`ALLOWED_HOSTS` no definido en production.py** — Depende 100% del `.env`. Si se despliega sin `.env` correcto, Django lanza error 500 sin mensaje claro | Difícil de debuggear en producción | Agregar fallback explícito o al menos un comentario de advertencia |
| BUG-8 | Todos los `tests.py` | **Cero tests** — Toda la lógica de negocio (`recalcular_avance`, `calcular_totales`, `OrdenCambio.aprobar`) está sin cubrir | Un refactor puede romper cálculos financieros sin que nadie lo detecte | Escribir tests para los 3 métodos críticos mínimamente |

---

## 🚧 FUNCIONALIDADES PENDIENTES (Post-MVP)

> Análisis comparativo PROMPT vs implementación actual. Porcentaje global: **~68% del spec completo**.

### 🔴 PRIORIDAD ALTA — Críticas para producto completo

| # | Módulo | Feature | Descripción |
|---|--------|---------|-------------|
| 1 | BD Costos | **Importar desde Excel** | Carga masiva de ítems desde .xlsx. Validación, preview, reporte errores. URL: `/bd-costos/importar/` |
| 2 | Reportes | **Exportar a Excel** | Multi-hoja: datos tabulados + gráficos + metadata. Criterio de éxito explícito en PROMPT §5.5 |
| 3 | Reportes | **Reporte Costos por Categoría** | Gráfico dona + tabla por tipo/categoría. Drill-down por proyecto. PROMPT §5.4 |

### 🟡 PRIORIDAD MEDIA — Importantes para v1.0

| # | Módulo | Feature | Descripción |
|---|--------|---------|-------------|
| 4 | Reportes | **Tendencia temporal cotizaciones** | Gráfico línea: cotizaciones enviadas por mes (últimos 12 meses). PROMPT §5.3 |
| 5 | Reportes | **KPIs faltantes** | Tiempo promedio de respuesta + valor promedio cotización. PROMPT §5.3 |
| 6 | Reportes | **Exportar reportes a PDF** | Generar PDF del reporte de rentabilidad. PROMPT §5.1 |
| 7 | BD Costos | **Exportar a Excel** | Respaldo/compartir BD costos en formato .xlsx. PROMPT §3.6 |
| 8 | Dashboard | **Sistema de alertas** | 4 tipos: cotizaciones sin seguimiento >5 días, proyectos próximos a entrega, rentabilidad negativa, variación costo >20%. PROMPT §4.3 |
| 9 | BD Costos | **Gráfico historial precios** | Línea Chart.js en modal historial (tabla ya existe). PROMPT §3.4 |

### 🟢 PRIORIDAD BAJA — UX/Polish

| # | Módulo | Feature | Descripción |
|---|--------|---------|-------------|
| 10 | Cotizaciones | **Autocompletado clientes** | Sugerir clientes de cotizaciones anteriores al escribir. PROMPT §2.2 |
| 11 | Proyectos | **Cronología visual** | Barra de progreso temporal [====>---] con hoy marcado. PROMPT §4.2 Tab 1 |
| 12 | BD Costos | **Drag & drop categorías** | Reordenar categorías arrastrando. PROMPT §3.3 |
| 13 | Proyectos | **Tab Cronograma** | Tabla de fechas por partida (decisión pendiente con cliente: Gantt vs tabla). PROMPT §4.2 Tab 3 |
| 14 | Proyectos | **Tab Equipo** | Lista de usuarios asignados al proyecto. PROMPT §4.2 Tab 6 |
| 15 | Cotizaciones | **Envío por email** | Enviar PDF al cliente por correo. PROMPT §2.2 (OPCIONAL) |

---

## 📊 COBERTURA POR MÓDULO

| Módulo | Implementado |
|--------|-------------|
| Core / Auth / Multi-tenant | 100% |
| Proyectos en Ejecución | 95% |
| BD de Costos (CRUD) | 90% |
| Seguridad Multi-tenant | 95% |
| Cotizaciones | 85% |
| Dashboard | 80% |
| UI / Diseño | 85% |
| Reportes | 55% |
| **TOTAL ESTIMADO** | **~68%** |

---

## 📝 DECISIONES TÉCNICAS

- **Django 6.0.3** (disponible en el entorno, no 5.x como el spec original)
- **UUID** como PK para modelos principales (mayor seguridad en URLs)
- **Soft delete** con campo `activo=True/False` en lugar de borrar físicamente
- **RegistroAvance** es inmutable (no se edita ni elimina, solo se crean ajustes)
- **ReportLab** para PDFs (programático, sin dependencias del sistema, funciona sin X11)
- **HTMX** para interactividad sin recargar página (partidas de cotización, búsquedas)
- **Alpine.js** para estado UI local (modales, validaciones front-end)

---

## ❓ PREGUNTAS PENDIENTES PARA EL CLIENTE

1. ¿Logo de la empresa para cotizaciones y reportes?
2. ¿Términos y condiciones estándar para cotizaciones? (garantía mencionada: 100 días)
3. ¿Necesita cronograma Gantt o tabla de fechas simple es suficiente?
4. ¿Módulo clientes separado o solo historial en cotizaciones?
5. ¿Prefiere moneda solo USD o también en Bs (VES)?

---

## 🗂️ ESTRUCTURA DE ARCHIVOS DEL PROYECTO

```
/home/sabh/Documentos/Smart/Smart Project Management/
├── env/                          ← Entorno virtual Python
├── smart_pm/                     ← Proyecto Django (en construcción)
├── files/                        ← Diseño HTML de referencia
│   ├── dashboard_principal.html
│   ├── nueva_cotizacion.html
│   ├── proyecto_ejecucion.html
│   └── reporte_financiero.html
├── PROYECTO_PROGRESO.md          ← Este archivo
├── PROMPT_SMART_PROJECT_MANAGEMENT.md
└── ANALISIS_INFORMACION_VALMORE.md
```
