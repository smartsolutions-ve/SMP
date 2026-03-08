# PROMPT COMPLETO: Smart Project Management System - MVP

> **Propósito de este documento:** Servir como contexto completo para Claude Code en su rol de arquitecto de software y desarrollador del sistema Smart Project Management. Este documento contiene únicamente especificaciones teóricas, arquitectura, modelo de datos, flujos de usuario y requisitos funcionales. NO contiene código de implementación.

---

## 📑 ÍNDICE

1. [Contexto del Proyecto](#contexto-del-proyecto)
2. [Cliente Principal: Valmore](#cliente-principal-balmore)
3. [Objetivos del Sistema](#objetivos-del-sistema)
4. [Arquitectura Técnica](#arquitectura-técnica)
5. [Modelo de Datos Completo](#modelo-de-datos-completo)
6. [Módulos Funcionales Detallados](#módulos-funcionales-detallados)
7. [Sistema de Roles y Permisos](#sistema-de-roles-y-permisos)
8. [Diseño de Interfaz de Usuario](#diseño-de-interfaz-de-usuario)
9. [Flujos de Usuario Críticos](#flujos-de-usuario-críticos)
10. [Requisitos No Funcionales](#requisitos-no-funcionales)
11. [Información Faltante y Preguntas Pendientes](#información-faltante-y-preguntas-pendientes)
12. [Criterios de Éxito](#criterios-de-éxito)

---

## 🎯 CONTEXTO DEL PROYECTO

### Empresa Desarrolladora
- **Nombre:** SmartSolutions VE
- **Ubicación:** Valencia, Carabobo, Venezuela
- **Desarrollador principal:** Simón Briceño
- **Socio comercial:** Javier Figueroa
- **Especialización:** Sistemas de gestión empresarial para PYMEs venezolanas

### Visión del Producto
"Smart Project Management" es un sistema web de gestión integral para empresas contratistas que busca reemplazar procesos manuales basados en Excel con una solución centralizada, profesional y escalable.

### Modelo de Negocio
- **Tipo:** SaaS (Software as a Service)
- **Precio implementación inicial:** $1,200 USD (pago único)
- **Suscripción mensual:** $100-120 USD/mes por empresa cliente
- **Mercado objetivo:** Contratistas de construcción, servicios profesionales, empresas de proyectos en Venezuela

### Versión Actual
**MVP (Minimum Viable Product) - Versión 1.0**
- Primera versión desarrollada específicamente para el cliente Valmore
- Sistema debe ser funcional y completo para las necesidades de Valmore
- Arquitectura preparada para escalar a múltiples clientes en el futuro

### Stack Tecnológico Definido
- **Backend:** Django 5.x (Python)
- **Base de datos:** PostgreSQL 16
- **Frontend:** HTMX + Alpine.js + Tailwind CSS
- **API:** Django REST Framework (para futuras integraciones)
- **Deployment:** DigitalOcean App Platform o VPS con Nginx + Gunicorn
- **Control de versiones:** Git

---

## 👤 CLIENTE PRINCIPAL: VALMORE

### Perfil de la Empresa

**Nombre de la empresa:** [PENDIENTE - Preguntar a Valmore]
- ¿Tiene razón social registrada?
- ¿Nombre comercial bajo el cual opera?

**Tipo de negocio:** Contratista de construcción
- **Ubicación:** Valencia, Carabobo, Venezuela
- **Tamaño:** [PENDIENTE] ¿Cuántos empleados?
- **Años en operación:** [PENDIENTE]

**Servicios que ofrece:**
[PENDIENTE - Información crítica a recopilar en entrevista]
- ¿Construcción de edificaciones nuevas?
- ¿Remodelaciones?
- ¿Mantenimiento?
- ¿Instalaciones especializadas (eléctricas, sanitarias, HVAC)?
- ¿Obra civil?
- ¿Trabajos especializados?

**Clientes típicos:**
[PENDIENTE]
- ¿Particulares (residencial)?
- ¿Empresas privadas (comercial)?
- ¿Sector público?
- ¿Desarrolladores inmobiliarios?

### Situación Actual (Problemas a Resolver)

**Proceso actual de cotizaciones:**
- Maneja cotizaciones en **hojas de cálculo Excel**
- [PENDIENTE] ¿Tiene plantilla estandarizada o cada cotización es desde cero?
- [PENDIENTE] ¿Cuántas cotizaciones genera al mes aproximadamente?
- [PENDIENTE] ¿Cuánto tiempo le toma crear una cotización típica?
- **Problema:** Sin historial centralizado, duplicación de trabajo, propenso a errores

**Base de datos de costos:**
- [PENDIENTE] ¿Cómo mantiene actualmente sus costos de materiales/mano de obra?
- [PENDIENTE] ¿Tiene archivo Excel con precios? ¿Está actualizado?
- [PENDIENTE] ¿Consulta proveedores cada vez que cotiza?
- **Problema:** Sin repositorio centralizado, precios desactualizados, difícil mantener márgenes

**Seguimiento de proyectos:**
- [PENDIENTE] ¿Cómo hace seguimiento actualmente? ¿Excel? ¿Papel? ¿WhatsApp?
- [PENDIENTE] ¿Tiene supervisores en campo? ¿Cómo reportan avance?
- [PENDIENTE] ¿Cada cuánto revisa avance vs presupuesto?
- **Problema:** Sin visibilidad en tiempo real, descubre problemas tarde, difícil controlar costos

**Reportes financieros:**
- [PENDIENTE] ¿Genera reportes de rentabilidad por proyecto?
- [PENDIENTE] ¿Sabe cuánto gana realmente en cada proyecto?
- **Problema:** Reportes manuales, consume mucho tiempo, datos incompletos

### Expectativas del Cliente

**Necesidades confirmadas:**
1. Crear cotizaciones profesionales rápidamente
2. Gestionar base de datos de costos centralizada
3. Hacer seguimiento del avance real de proyectos
4. Comparar costos presupuestados vs reales
5. Generar reportes financieros automáticos

**Necesidades a validar en entrevista:**
[PENDIENTE - Responder con cuestionario de 50 preguntas ya preparado]
- ¿Necesita control de inventario de materiales?
- ¿Necesita gestión de proveedores?
- ¿Necesita control de asistencia de personal?
- ¿Necesita cronograma Gantt detallado?
- ¿Necesita facturación integrada? (NOTA: módulo fiscal requiere homologación SENIAT, fuera del MVP)
- ¿Necesita gestión de múltiples obras simultáneas?
- ¿Necesita subir fotos de avance?
- ¿Necesita firmas digitales en documentos?
- ¿Necesita app móvil o web responsive es suficiente?

### Información Operativa Faltante

**Volúmenes de operación:**
[PENDIENTE - Crítico para dimensionar sistema]
- ¿Cuántas cotizaciones genera por mes?
- ¿Cuántos proyectos maneja simultáneamente?
- ¿Cuántos proyectos completa por año?
- ¿Cuál es el valor promedio de un proyecto?
- ¿Proyecto más pequeño y más grande que ha ejecutado?
- ¿Duración típica de un proyecto?

**Equipo de trabajo:**
[PENDIENTE]
- ¿Cuántas personas necesitan acceso al sistema?
- ¿Roles actuales en la empresa? (gerente, supervisor, administrativo, etc.)
- ¿Quién crea las cotizaciones actualmente?
- ¿Quién hace seguimiento de obra?
- ¿Quién genera reportes?

**Procesos específicos:**
[PENDIENTE - Para diseñar flujos correctos]
- Flujo completo: Cliente solicita presupuesto → ¿Qué pasa?
- Cuando ganan un proyecto: ¿Cómo se formaliza? ¿Contrato? ¿Anticipo?
- Durante ejecución: ¿Cómo registran avance? ¿Cada cuánto?
- ¿Manejan órdenes de cambio? ¿Cómo se aprueban?
- Al terminar proyecto: ¿Proceso de cierre? ¿Garantías?

**Estructura de costos:**
[PENDIENTE - Para diseñar BD de costos correctamente]
- ¿Qué categorías principales de costos maneja?
  - Materiales
  - Mano de obra (¿por hora? ¿por tarea? ¿subcontratada?)
  - Equipos (¿propios? ¿alquilados?)
  - Subcontratos especializados
  - Otros
- ¿Cómo calcula mano de obra? ¿Tiene cuadrillas fijas?
- ¿Equipos propios o alquilados?
- ¿Trabaja con subcontratistas? ¿Para qué rubros?

**Formato de cotizaciones:**
[PENDIENTE - Para generar PDFs correctos]
- ¿Tiene formato/plantilla que le guste?
- ¿Puede compartir ejemplo de cotización actual?
- ¿Qué información incluye siempre?
- ¿Logo de empresa? ¿Puede compartirlo?
- ¿Términos y condiciones estándar?
- ¿Forma de pago típica? (anticipo, avances, contraentrega)
- ¿Garantías que ofrece?

---

## 🎯 OBJETIVOS DEL SISTEMA

### Objetivos Primarios (MVP)

1. **Eliminar dependencia de Excel** para cotizaciones y seguimiento
2. **Centralizar información** de costos, proyectos y clientes
3. **Acelerar creación de cotizaciones** de horas a minutos
4. **Visibilidad en tiempo real** del avance y rentabilidad de proyectos
5. **Profesionalizar imagen** con cotizaciones y reportes de calidad

### Objetivos Secundarios (Post-MVP)

- Integración con sistema de facturación homologado SENIAT
- App móvil nativa para supervisores en campo
- Integración con software de contabilidad
- Sistema de notificaciones automáticas
- Portal de cliente (acceso externo para clientes ver su proyecto)

### Objetivos de Negocio para SmartSolutions VE

1. **Probar modelo de negocio SaaS** con cliente real (Valmore)
2. **Validar arquitectura multi-tenant** para escalabilidad futura
3. **Crear caso de éxito** documentado para captar más clientes
4. **Establecer base de código** reutilizable para futuras implementaciones
5. **Lograr que Valmore elimine Excel en 100%** en 3 meses de uso

---

## 🏗️ ARQUITECTURA TÉCNICA

### Decisión Arquitectónica: Multi-Tenant Pragmático

**Enfoque adoptado:** Multi-tenant desde la base de datos, single-tenant en operación inicial

**Justificación:**
- Sistema técnicamente preparado para múltiples clientes desde día 1
- Cada tabla incluye campo `empresa` para aislamiento de datos
- Middleware de tenant implementado desde el inicio
- Sin complejidad de subdominios en fase MVP
- Cuando llegue cliente #2, solo se requiere configuración, no rediseño

**Implementación:**
- Todas las entidades del dominio tienen relación con `Empresa`
- Queries automáticamente filtrados por empresa actual
- Middleware identifica empresa del usuario autenticado
- Sistema de permisos valida acceso solo a datos de su empresa

### Capas de la Aplicación

```
┌─────────────────────────────────────────────┐
│         CAPA DE PRESENTACIÓN                │
│  (Templates Django + HTMX + Alpine.js)      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│          CAPA DE APLICACIÓN                 │
│     (Views, Forms, Serializers)             │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         CAPA DE DOMINIO                     │
│  (Models, Business Logic, Managers)         │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         CAPA DE PERSISTENCIA                │
│         (PostgreSQL Database)               │
└─────────────────────────────────────────────┘
```

### Separación en Apps Django

**Apps principales del sistema:**

1. **`core`** - Funcionalidad compartida
   - Modelo `Empresa` (tenant)
   - Modelo `User` (extendido de AbstractUser)
   - Middleware de tenant
   - Decoradores de permisos
   - Utilidades compartidas
   - Templates base

2. **`cotizaciones`** - Sistema de cotizaciones
   - Modelo `Cotizacion`
   - Modelo `PartidaCotizacion`
   - Generación de PDFs
   - Estados y flujo de aprobación

3. **`bd_costos`** - Base de datos de costos
   - Modelo `ItemCosto`
   - Modelo `CategoriaItem`
   - Modelo `HistorialPrecio`
   - Import/export Excel

4. **`proyectos`** - Gestión de proyectos
   - Modelo `Proyecto`
   - Modelo `PartidaProyecto`
   - Modelo `RegistroAvance`
   - Modelo `FotoProyecto`
   - Modelo `OrdenCambio`

5. **`reportes`** - Reportes y analytics
   - Views de reportes
   - Generación de gráficos
   - Export a Excel
   - Cálculos de KPIs

### Patrones de Diseño Aplicados

**1. Repository Pattern (via Django Managers)**
- Managers personalizados para queries complejas
- Encapsulación de lógica de acceso a datos
- Filtrado automático por tenant en manager base

**2. Service Layer**
- Lógica de negocio compleja fuera de Views
- Servicios reutilizables (ej: `CotizacionService`, `ProyectoService`)
- Transacciones atómicas en operaciones multi-modelo

**3. Decoradores para Cross-Cutting Concerns**
- `@requiere_rol(...)` para autorización
- `@tenant_required` para validar acceso
- `@transaction.atomic` para consistencia

**4. Template Method (en generación de documentos)**
- Clase base `DocumentGenerator`
- Subclases: `CotizacionPDFGenerator`, `ReporteExcelGenerator`

### Estructura de Directorios Propuesta

```
smart_project_management/
│
├── config/                          # Configuración del proyecto
│   ├── settings/
│   │   ├── base.py                 # Settings comunes
│   │   ├── development.py          # Settings desarrollo
│   │   └── production.py           # Settings producción
│   ├── urls.py                     # URLs raíz
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                            # Aplicaciones Django
│   ├── core/                       # App principal
│   │   ├── models.py              # Empresa, User
│   │   ├── middleware.py          # TenantMiddleware
│   │   ├── managers.py            # TenantManager (base)
│   │   ├── decorators.py          # @requiere_rol, @tenant_required
│   │   ├── views.py               # Login, Dashboard
│   │   ├── urls.py
│   │   └── templates/core/
│   │
│   ├── cotizaciones/              # Sistema cotizaciones
│   │   ├── models.py              # Cotizacion, PartidaCotizacion
│   │   ├── views.py               # CRUD cotizaciones
│   │   ├── forms.py               # Forms de cotización
│   │   ├── services.py            # CotizacionService
│   │   ├── pdf_generator.py      # Generación PDFs
│   │   ├── urls.py
│   │   └── templates/cotizaciones/
│   │
│   ├── bd_costos/                 # BD costos
│   │   ├── models.py              # ItemCosto, CategoriaItem
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── importers.py           # Import Excel
│   │   ├── exporters.py           # Export Excel
│   │   ├── urls.py
│   │   └── templates/bd_costos/
│   │
│   ├── proyectos/                 # Gestión proyectos
│   │   ├── models.py              # Proyecto, PartidaProyecto, etc.
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── services.py            # ProyectoService
│   │   ├── calculators.py         # Cálculos de avance, costos
│   │   ├── urls.py
│   │   └── templates/proyectos/
│   │
│   └── reportes/                  # Reportes
│       ├── views.py
│       ├── generators.py          # Generadores de reportes
│       ├── calculators.py         # KPIs, métricas
│       ├── excel_exporter.py
│       ├── urls.py
│       └── templates/reportes/
│
├── static/                         # Archivos estáticos
│   ├── css/
│   │   └── styles.css             # Tailwind compilado + custom
│   ├── js/
│   │   ├── htmx.min.js
│   │   ├── alpine.min.js
│   │   ├── chart.min.js
│   │   └── app.js                 # JS custom si necesario
│   └── img/
│       └── logo.png
│
├── templates/                      # Templates globales
│   ├── base.html                  # Template base
│   ├── dashboard.html             # Dashboard principal
│   └── components/                # Componentes reutilizables
│       ├── navbar.html
│       ├── sidebar.html
│       ├── modal.html
│       └── table.html
│
├── media/                          # Archivos subidos
│   ├── proyectos/                 # Fotos de proyectos
│   └── logos/                     # Logos de empresas
│
├── requirements/                   # Dependencias
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
│
├── docs/                           # Documentación
│   ├── architecture.md
│   ├── database_schema.md
│   ├── user_manual.pdf
│   └── deployment.md
│
├── scripts/                        # Scripts utilidad
│   ├── create_demo_data.py
│   └── backup_db.sh
│
├── .env.example                    # Variables entorno ejemplo
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt                # Dependencias principales
```

### Seguridad Multi-Tenant

**Principios implementados:**

1. **Aislamiento en capa de base de datos**
   - Todo modelo con relación a `Empresa`
   - Manager base filtra automáticamente por `empresa`
   - Imposible hacer query sin filtro de empresa

2. **Validación en capa de aplicación**
   - Middleware valida que `request.user.empresa` existe
   - Views validan que objetos accedidos pertenecen a empresa del usuario
   - Forms validan que ForeignKeys pertenecen a empresa correcta

3. **Validación en capa de presentación**
   - Templates solo muestran datos de empresa actual
   - Links/forms incluyen validación de pertenencia

**Ejemplo de flujo de seguridad:**

```
Usuario Valmore intenta editar Proyecto ID=5

1. MIDDLEWARE: Identifica empresa = "Construcciones Valmore"
2. VIEW: Hace query Proyecto.objects.get(id=5, empresa=request.tenant)
   - Si proyecto no pertenece a su empresa → 404 Not Found
   - Si pertenece → continúa
3. FORM: Al guardar cambios, valida que todas las relaciones 
   (ej: partidas) pertenecen a misma empresa
4. TEMPLATE: Solo muestra opciones (selects) de su empresa
```

---

## 💾 MODELO DE DATOS COMPLETO

### Principios del Modelo de Datos

1. **Normalización:** Base de datos normalizada hasta 3FN mínimo
2. **Auditoría:** Todos los modelos principales con campos de auditoría
3. **Soft delete:** No eliminación física, usar flags `activo`/`eliminado`
4. **Inmutabilidad selectiva:** Algunos registros no se pueden editar una vez creados (ej: registros de avance)
5. **Historización:** Mantener historial donde sea relevante (ej: precios)

### Modelo: Empresa (Tenant)

**Propósito:** Entidad raíz del sistema multi-tenant. Representa cada empresa cliente.

**Relaciones:**
- Un `User` pertenece a una `Empresa`
- Todas las entidades del dominio pertenecen a una `Empresa`

**Campos principales:**
- `id`: Identificador único (UUID recomendado)
- `nombre`: Razón social o nombre comercial
- `rif`: RIF fiscal venezolano (ej: J-12345678-9)
- `direccion`: Dirección física
- `telefono`: Teléfono principal
- `email`: Email de contacto
- `sitio_web`: URL del sitio web (opcional)
- `logo`: Imagen del logo (para cotizaciones y reportes)
- `fecha_creacion`: Timestamp de creación
- `activo`: Boolean (para desactivar sin eliminar)

**Campos de configuración:**
- `moneda_default`: USD o VES (default: USD)
- `margen_utilidad_default`: Decimal (ej: 15.00 para 15%)
- `terminos_condiciones_default`: Texto largo con T&C para cotizaciones

**Reglas de negocio:**
- RIF debe ser único en el sistema
- Al crear empresa, debe tener al menos un usuario Admin
- No se puede eliminar empresa con proyectos activos

---

### Modelo: Usuario (User)

**Propósito:** Usuarios del sistema que pertenecen a una empresa.

**Hereda de:** `AbstractUser` de Django (incluye username, email, password, etc.)

**Campos adicionales:**
- `empresa`: ForeignKey a `Empresa`
- `rol`: CharField con choices (ADMIN, GERENTE, SUPERVISOR, CLIENTE)
- `telefono`: CharField (opcional)
- `foto_perfil`: ImageField (opcional)
- `activo`: Boolean (heredado, pero importante)

**Roles y sus capacidades:**

**ADMIN:**
- Acceso total al sistema
- Gestión de usuarios de su empresa
- Configuración de empresa
- Todos los permisos de otros roles

**GERENTE:**
- Crear/editar cotizaciones
- Crear/editar proyectos
- Gestionar BD de costos
- Ver todos los reportes
- No puede gestionar usuarios ni configuración

**SUPERVISOR:**
- Ver proyectos asignados (solo lectura cotizaciones)
- Registrar avances en proyectos
- Subir fotos de progreso
- Ver BD de costos (solo lectura)

**CLIENTE (acceso externo):**
- Ver sus cotizaciones (solo lectura)
- Ver avance de su proyecto (solo lectura)
- Descargar PDFs

**Reglas de negocio:**
- Username debe ser único en toda la aplicación
- Email debe ser único por empresa
- Al menos un usuario con rol ADMIN por empresa
- No se puede cambiar de empresa una vez asignado

---

### Modelo: CategoriaItem

**Propósito:** Organización jerárquica de ítems de costo.

**Campos:**
- `id`: Identificador único
- `empresa`: ForeignKey a `Empresa`
- `nombre`: Nombre de la categoría (ej: "Preliminares", "Estructura")
- `codigo`: Código alfanumérico (ej: "01", "02.01")
- `padre`: ForeignKey a sí misma (self-reference, null=True) para jerarquía
- `descripcion`: TextField (opcional)
- `activo`: Boolean

**Estructura jerárquica ejemplo:**
```
01 - PRELIMINARES
  01.01 - Limpieza de terreno
  01.02 - Replanteo
  01.03 - Excavaciones
02 - ESTRUCTURA
  02.01 - Fundaciones
  02.02 - Columnas
  02.03 - Vigas
03 - ALBAÑILERÍA
  03.01 - Paredes
  03.02 - Frisos
```

**Reglas de negocio:**
- Código único por empresa
- No se puede eliminar categoría con ítems asociados
- Máximo 3 niveles de profundidad

---

### Modelo: ItemCosto

**Propósito:** Repositorio central de costos unitarios (materiales, mano de obra, equipos, etc.)

**Campos principales:**
- `id`: Identificador único
- `empresa`: ForeignKey a `Empresa`
- `codigo`: Código alfanumérico único (ej: "MAT-001", "MO-010")
- `descripcion`: Descripción completa del ítem
- `tipo`: CharField con choices (MATERIAL, MANO_OBRA, EQUIPO, SUBCONTRATO, OTROS)
- `categoria`: ForeignKey a `CategoriaItem` (nullable)
- `unidad`: CharField (m2, m3, kg, un, día, hora, etc.)
- `precio_actual`: Decimal (precio vigente)
- `moneda`: CharField (USD o VES)
- `fecha_actualizacion`: DateField (auto_now)
- `especificaciones`: TextField (detalles técnicos, opcional)
- `proveedor_preferido`: CharField (opcional)
- `notas`: TextField (opcional)
- `activo`: Boolean
- `creado_por`: ForeignKey a `User`
- `fecha_creacion`: DateTimeField

**Validaciones:**
- Código único por empresa
- Precio debe ser > 0
- Unidad debe ser de lista predefinida o personalizable

**Índices importantes:**
- `(empresa, codigo)` - búsqueda rápida por código
- `(empresa, descripcion)` - búsqueda por texto
- `(empresa, tipo)` - filtrado por tipo

---

### Modelo: HistorialPrecio

**Propósito:** Mantener histórico de cambios de precios para análisis de tendencias.

**Campos:**
- `id`: Identificador único
- `item`: ForeignKey a `ItemCosto`
- `fecha`: DateField (fecha del cambio)
- `precio`: Decimal (precio en esa fecha)
- `moneda`: CharField
- `observacion`: CharField (razón del cambio, opcional)
- `usuario`: ForeignKey a `User` (quién hizo el cambio)

**Reglas de negocio:**
- Se crea automáticamente cada vez que cambia `precio_actual` de un `ItemCosto`
- No se puede editar ni eliminar (registro de auditoría)
- Útil para gráficos de tendencias de precios

---

### Modelo: Cotizacion

**Propósito:** Presupuesto/propuesta comercial para un cliente potencial.

**Campos principales:**

**Identificación:**
- `id`: Identificador único
- `empresa`: ForeignKey a `Empresa`
- `numero`: CharField único (ej: "COT-2024-001")
- `fecha_creacion`: DateField
- `fecha_vencimiento`: DateField (validez de la oferta)

**Cliente:**
- `cliente_nombre`: CharField (nombre/razón social)
- `cliente_rif`: CharField (opcional)
- `cliente_direccion`: TextField
- `cliente_telefono`: CharField
- `cliente_email`: EmailField (opcional)
- `cliente_contacto`: CharField (persona de contacto, opcional)

**Proyecto:**
- `nombre_proyecto`: CharField (ej: "Remodelación Oficina Principal")
- `descripcion`: TextField (alcance general)
- `ubicacion`: CharField (dirección o zona)

**Estado:**
- `estado`: CharField con choices:
  - `BORRADOR`: En edición, no enviada
  - `ENVIADA`: Enviada al cliente
  - `APROBADA`: Cliente aceptó
  - `RECHAZADA`: Cliente rechazó
  - `VENCIDA`: Pasó fecha_vencimiento sin respuesta
  - `CONVERTIDA`: Ya se convirtió en proyecto

**Financiero:**
- `subtotal`: Decimal (suma de todas las partidas)
- `margen_utilidad_porcentaje`: Decimal (ej: 15.00)
- `utilidad_monto`: Decimal (calculado)
- `total`: Decimal (subtotal + utilidad)
- `moneda`: CharField (USD o VES)

**Términos:**
- `terminos_condiciones`: TextField (forma de pago, garantías, etc.)
- `notas_internas`: TextField (no visible al cliente)

**Seguimiento:**
- `fecha_envio`: DateTimeField (nullable, cuando se envía)
- `fecha_respuesta`: DateTimeField (nullable, cuando cliente responde)
- `observaciones_cliente`: TextField (feedback del cliente, opcional)

**Auditoría:**
- `creado_por`: ForeignKey a `User`
- `modificado_por`: ForeignKey a `User` (nullable)
- `fecha_modificacion`: DateTimeField (auto_now)

**Reglas de negocio:**
- Número único por empresa (puede ser secuencial: COT-YYYY-NNN)
- No se puede editar cotización en estado APROBADA o CONVERTIDA
- No se puede eliminar cotización CONVERTIDA (tiene proyecto asociado)
- Al cambiar a estado ENVIADA, registrar fecha_envio
- Calcular automáticamente: utilidad_monto = subtotal × (margen_utilidad_porcentaje / 100)
- Calcular automáticamente: total = subtotal + utilidad_monto

**Métodos importantes:**
- `calcular_totales()`: Recalcula subtotal, utilidad, total
- `puede_editarse()`: Retorna si está en estado editable
- `convertir_a_proyecto()`: Crea Proyecto asociado

---

### Modelo: PartidaCotizacion

**Propósito:** Línea individual de trabajo/material en una cotización.

**Campos:**
- `id`: Identificador único
- `cotizacion`: ForeignKey a `Cotizacion` (on_delete=CASCADE)
- `orden`: PositiveIntegerField (para mantener orden visual)
- `item_costo`: ForeignKey a `ItemCosto` (nullable, si viene de BD de costos)
- `codigo`: CharField (código del ítem, puede copiarse de ItemCosto)
- `descripcion`: CharField (descripción, puede copiarse o editarse)
- `unidad`: CharField
- `categoria`: CharField (para agrupar en PDF: Preliminares, Estructura, etc.)
- `cantidad`: Decimal
- `precio_unitario`: Decimal
- `subtotal`: Decimal (calculado: cantidad × precio_unitario)

**Reglas de negocio:**
- Subtotal calculado automáticamente al guardar
- Orden debe ser único dentro de la cotización
- Si `item_costo` es nulo, significa que es partida custom (no de BD)
- Al cambiar cantidad o precio_unitario, recalcular subtotal
- Al agregar/eliminar partida, recalcular totales de cotización

**Ordenamiento:**
- Por defecto ordenar por campo `orden`
- Permitir reordenar (drag & drop en UI)

---

### Modelo: Proyecto

**Propósito:** Trabajo real en ejecución, convertido desde una cotización aprobada.

**Campos principales:**

**Identificación:**
- `id`: Identificador único
- `empresa`: ForeignKey a `Empresa`
- `cotizacion_origen`: ForeignKey a `Cotizacion` (nullable, pero normalmente presente)
- `codigo`: CharField único (ej: "PROY-2024-001")
- `nombre`: CharField
- `descripcion`: TextField
- `ubicacion`: CharField

**Cliente:**
- `cliente_nombre`: CharField
- `cliente_rif`: CharField (opcional)
- `cliente_contacto`: CharField (persona responsable)
- `cliente_telefono`: CharField
- `cliente_email`: EmailField (opcional)

**Fechas:**
- `fecha_inicio_planeada`: DateField
- `fecha_inicio_real`: DateField (nullable, se llena al iniciar)
- `fecha_fin_planeada`: DateField
- `fecha_fin_real`: DateField (nullable, se llena al completar)

**Financiero:**
- `valor_contrato`: Decimal (monto total acordado con cliente)
- `moneda`: CharField (USD o VES)

**Estado:**
- `estado`: CharField con choices:
  - `PLANIFICACION`: Proyecto creado, no iniciado
  - `EN_EJECUCION`: Trabajo en progreso
  - `PAUSADO`: Temporalmente detenido
  - `COMPLETADO`: Trabajo terminado
  - `CANCELADO`: Proyecto cancelado

**Control:**
- `porcentaje_avance`: Decimal (0.00 a 100.00, calculado desde partidas)

**Equipo:**
- `gerente_proyecto`: ForeignKey a `User` (responsable principal)
- `supervisor`: ForeignKey a `User` (nullable, supervisor en campo)

**Auditoría:**
- `creado_por`: ForeignKey a `User`
- `fecha_creacion`: DateTimeField

**Campos calculados (properties):**
- `costo_real_total`: Suma de costos reales de todas las partidas
- `utilidad_real`: `valor_contrato - costo_real_total`
- `margen_real_porcentaje`: `(utilidad_real / valor_contrato) × 100`
- `dias_transcurridos`: Desde fecha_inicio_real hasta hoy
- `dias_restantes`: Desde hoy hasta fecha_fin_planeada
- `esta_atrasado`: Boolean (fecha_fin_planeada < hoy y estado != COMPLETADO)

**Reglas de negocio:**
- Código único por empresa
- No se puede eliminar proyecto (soft delete con estado CANCELADO)
- Al cambiar a EN_EJECUCION, llenar fecha_inicio_real
- Al cambiar a COMPLETADO, llenar fecha_fin_real
- Recalcular porcentaje_avance cada vez que se actualiza partida

---

### Modelo: PartidaProyecto

**Propósito:** Línea de trabajo en ejecución real, basada en cotización pero con datos de ejecución.

**Campos de presupuesto (origen):**
- `id`: Identificador único
- `proyecto`: ForeignKey a `Proyecto` (on_delete=CASCADE)
- `codigo`: CharField
- `descripcion`: CharField
- `unidad`: CharField
- `categoria`: CharField
- `cantidad_presupuestada`: Decimal (lo que se cotizó)
- `precio_unitario_presupuestado`: Decimal
- `costo_presupuestado`: Decimal (cantidad × precio_unitario)

**Campos de ejecución (real):**
- `cantidad_ejecutada`: Decimal (default: 0)
- `costo_real`: Decimal (default: 0) - suma de costos de registros de avance

**Estado:**
- `estado`: CharField con choices:
  - `NO_INICIADA`: No se ha trabajado
  - `EN_PROCESO`: Se está ejecutando
  - `COMPLETADA`: Terminada
- `porcentaje_avance`: Decimal (0-100, calculado desde registros de avance)

**Campos calculados (properties):**
- `variacion_cantidad`: `cantidad_ejecutada - cantidad_presupuestada`
- `variacion_costo`: `costo_real - costo_presupuestado`
- `variacion_porcentaje`: `(variacion_costo / costo_presupuestado) × 100`

**Reglas de negocio:**
- Se crean automáticamente desde PartidaCotizacion al convertir cotización
- `cantidad_ejecutada` y `costo_real` se actualizan desde RegistroAvance
- `porcentaje_avance = (cantidad_ejecutada / cantidad_presupuestada) × 100`
- Estado cambia automáticamente:
  - Si porcentaje_avance > 0 y < 100 → EN_PROCESO
  - Si porcentaje_avance >= 100 → COMPLETADA
  - Si porcentaje_avance == 0 → NO_INICIADA

---

### Modelo: RegistroAvance

**Propósito:** Registro diario/periódico del progreso de una partida. Inmutable una vez guardado.

**Campos:**
- `id`: Identificador único
- `partida`: ForeignKey a `PartidaProyecto` (on_delete=PROTECT)
- `fecha`: DateField
- `cantidad_ejecutada_dia`: Decimal (avance de ese día en unidades de la partida)
- `costo_dia`: Decimal (costo real incurrido ese día)
- `observaciones`: TextField (opcional, comentarios del supervisor)
- `registrado_por`: ForeignKey a `User`
- `fecha_registro`: DateTimeField (auto_now_add, cuándo se hizo el registro)

**Reglas de negocio:**
- NO se puede editar ni eliminar una vez guardado (inmutable para auditoría)
- Al guardar, actualizar automáticamente:
  - `partida.cantidad_ejecutada += cantidad_ejecutada_dia`
  - `partida.costo_real += costo_dia`
  - Recalcular `partida.porcentaje_avance`
  - Recalcular `proyecto.porcentaje_avance`
- Si se necesita corregir, crear nuevo registro con valores negativos (ajuste)

---

### Modelo: FotoProyecto

**Propósito:** Evidencia fotográfica del avance del proyecto.

**Campos:**
- `id`: Identificador único
- `proyecto`: ForeignKey a `Proyecto`
- `fecha`: DateField (auto_now_add)
- `descripcion`: CharField (ej: "Avance estructura segundo piso")
- `imagen`: ImageField (upload_to='proyectos/{proyecto_id}/{año}/{mes}/')
- `subido_por`: ForeignKey a `User`

**Reglas de negocio:**
- Imágenes se comprimen automáticamente al subir (max 1920px ancho)
- Metadata EXIF preservada si contiene GPS
- Se pueden agregar múltiples fotos por día
- Asociadas al proyecto, no a partida específica (simplifica)

---

### Modelo: OrdenCambio

**Propósito:** Cambios al alcance original del proyecto que afectan costo o tiempo.

**Campos:**
- `id`: Identificador único
- `proyecto`: ForeignKey a `Proyecto`
- `numero`: PositiveIntegerField (secuencial por proyecto: 1, 2, 3...)
- `fecha`: DateField (auto_now_add)
- `descripcion`: TextField (qué se va a cambiar)
- `justificacion`: TextField (por qué es necesario)
- `impacto_costo`: Decimal (positivo o negativo, en moneda del proyecto)
- `impacto_tiempo_dias`: IntegerField (positivo o negativo)
- `estado`: CharField con choices:
  - `PENDIENTE`: Esperando aprobación
  - `APROBADA`: Aceptada, se aplica
  - `RECHAZADA`: No se aplicará
- `aprobado_por`: ForeignKey a `User` (nullable, quien aprueba)
- `fecha_aprobacion`: DateField (nullable)
- `observaciones_aprobacion`: TextField (opcional)
- `solicitado_por`: ForeignKey a `User`

**Reglas de negocio:**
- Número debe ser único dentro del proyecto
- Solo usuarios con rol ADMIN o GERENTE pueden aprobar
- Al aprobar con impacto positivo de costo:
  - `proyecto.valor_contrato += impacto_costo`
- Al aprobar con impacto de tiempo:
  - `proyecto.fecha_fin_planeada += impacto_tiempo_dias`
- No se puede editar una vez aprobada o rechazada

---

## 📐 MÓDULOS FUNCIONALES DETALLADOS

### MÓDULO 1: Dashboard Principal

**URL:** `/dashboard/`

**Propósito:** Vista de entrada al sistema que muestra estado general de la empresa.

**Audiencia:** Todos los roles (contenido adaptado según permisos)

**Secciones de contenido:**

**1. Header con stats principales (4 cards)**
```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Proyectos    │ Cotizaciones │ Valor en     │ Rentabilidad │
│ Activos      │ Pendientes   │ Ejecución    │ Promedio     │
│   [8]        │   [12]       │ [$128.5K]    │   [18.2%]    │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

**Cálculos:**
- **Proyectos Activos:** COUNT de `Proyecto` con `estado IN (PLANIFICACION, EN_EJECUCION, PAUSADO)`
- **Cotizaciones Pendientes:** COUNT de `Cotizacion` con `estado IN (BORRADOR, ENVIADA)`
- **Valor en Ejecución:** SUM de `Proyecto.valor_contrato` donde `estado = EN_EJECUCION`
- **Rentabilidad Promedio:** PROMEDIO de `margen_real_porcentaje` de proyectos en ejecución

**2. Lista de proyectos en ejecución**
Tabla con:
- Nombre del proyecto
- Barra de progreso visual (% de avance)
- Estado de timing (En tiempo / Atrasado X días)
- Valor del contrato
- Rentabilidad actual
- Acciones rápidas (Ver detalle, Registrar avance)

**3. Alertas y notificaciones**
Sistema de alertas configurables:
- Cotizaciones sin seguimiento > 5 días
- Proyectos próximos a fecha de entrega (< 7 días)
- Proyectos con rentabilidad negativa
- Partidas con variación de costo > 20%
- [PENDIENTE - Confirmar con Valmore qué alertas son prioritarias]

**4. Gráfico de tendencias (opcional en MVP)**
- Eje X: Meses
- Eje Y: Valor de proyectos
- Líneas: Proyectos nuevos, Proyectos completados, Valor total

**Roles y permisos:**
- **ADMIN/GERENTE:** Ven todo
- **SUPERVISOR:** Solo proyectos donde está asignado como supervisor
- **CLIENTE:** No accede a este dashboard (tiene vista especializada)

---

### MÓDULO 2: Sistema de Cotizaciones

**URLs principales:**
- `/cotizaciones/` - Lista de cotizaciones
- `/cotizaciones/nueva/` - Crear cotización
- `/cotizaciones/<id>/` - Ver detalle
- `/cotizaciones/<id>/editar/` - Editar
- `/cotizaciones/<id>/duplicar/` - Duplicar
- `/cotizaciones/<id>/pdf/` - Descargar PDF
- `/cotizaciones/<id>/enviar/` - Enviar por email
- `/cotizaciones/<id>/convertir-proyecto/` - Convertir a proyecto

#### 2.1. Vista de Lista

**Propósito:** Ver todas las cotizaciones con filtros y búsqueda.

**Filtros disponibles:**
- Estado (Todas, Borrador, Enviada, Aprobada, Rechazada, Vencida)
- Rango de fechas (creación o vencimiento)
- Cliente (búsqueda por nombre)
- Valor (rango mínimo-máximo)

**Información mostrada en tabla:**
- Número de cotización
- Cliente
- Proyecto
- Fecha creación
- Fecha vencimiento
- Total
- Estado (badge con color)
- Acciones (Ver, Editar, PDF, Más opciones)

**Ordenamiento:**
- Por defecto: Más recientes primero
- Permitir ordenar por: Fecha, Total, Estado, Cliente

**Paginación:** 20 cotizaciones por página

#### 2.2. Crear/Editar Cotización

**Paso 1: Datos básicos**

**Sección Cliente:**
- Nombre/Razón social (requerido)
- RIF (opcional)
- Dirección (requerido)
- Teléfono (requerido)
- Email (opcional)
- Persona de contacto (opcional)

**MEJORA UX:** Autocompletar desde clientes anteriores
[PENDIENTE - ¿Valmore querría un módulo de Clientes separado o solo historial en cotizaciones?]

**Sección Proyecto:**
- Nombre del proyecto (requerido)
- Descripción del alcance (requerido, textarea)
- Ubicación (requerido)
- Fecha de vencimiento (requerido, default: +15 días)

**Paso 2: Agregar partidas**

**Opción A: Desde BD de costos**
- Modal de búsqueda de ItemCosto
- Buscador con filtro por código/descripción/tipo
- Al seleccionar:
  - Copiar: código, descripción, unidad, precio_actual
  - Usuario ajusta: cantidad, precio si es necesario

**Opción B: Partida manual**
- Formulario inline:
  - Código (opcional)
  - Descripción (requerido)
  - Unidad (requerido)
  - Cantidad (requerido)
  - Precio unitario (requerido)
  - Categoría (select, para agrupar en PDF)

**Tabla de partidas:**
```
┌────────┬──────────────────────┬────────┬──────────┬────────────┬────────────┬──────────┐
│ Código │ Descripción          │ Unidad │ Cantidad │ P.Unit     │ Subtotal   │ Acciones │
├────────┼──────────────────────┼────────┼──────────┼────────────┼────────────┼──────────┤
│ 01.01  │ Limpieza de terreno  │ m2     │   250.00 │ $    2.50  │ $   625.00 │ [Edit][X]│
│ 01.02  │ Replanteo y nivelac. │ m2     │   250.00 │ $    1.80  │ $   450.00 │ [Edit][X]│
│ 02.01  │ Excavación manual    │ m3     │    45.00 │ $   12.00  │ $   540.00 │ [Edit][X]│
└────────┴──────────────────────┴────────┴──────────┴────────────┴────────────┴──────────┘
                                                          Subtotal: $ 1,615.00
                                      Utilidad (15.00%): $   242.25
                                                TOTAL: $ 1,857.25
```

**Cálculo automático con HTMX:**
- Al cambiar cantidad o precio unitario de partida → recalcular subtotal de partida
- Al agregar/eliminar partida → recalcular subtotal general
- Al cambiar margen de utilidad → recalcular utilidad y total
- Todo sin recargar página (HTMX)

**Paso 3: Configuración final**

**Margen de utilidad:**
- Input numérico (porcentaje)
- Default: `empresa.margen_utilidad_default`
- Editable por usuario

**Términos y condiciones:**
- Textarea
- Default: `empresa.terminos_condiciones_default`
- Editable por usuario
- Ejemplo de contenido:
```
VALIDEZ DE LA OFERTA: 15 días calendario

FORMA DE PAGO:
- 30% anticipo contra firma de contrato
- 40% contra avance de obra (a definir según cronograma)
- 30% contraentrega y recepción final

PLAZO DE EJECUCIÓN: Según cronograma a presentar

GARANTÍA: 6 meses contra defectos de construcción

NO INCLUYE:
- Permisos y tramitología municipal
- Estudios de suelo
- Acometidas de servicios públicos
```

**Notas internas:**
- Textarea (opcional)
- No visible en PDF ni para cliente
- Para uso interno (ej: "Cliente mencionó presupuesto limitado", "Competidor cotizó $X")

**Paso 4: Acciones finales**

**Guardar como Borrador:**
- Estado = BORRADOR
- Permite seguir editando después
- No registra fecha_envio

**Generar y Enviar:**
- Validar que todos los campos requeridos estén completos
- Generar PDF automáticamente
- Cambiar estado = ENVIADA
- Registrar fecha_envio
- [OPCIONAL] Enviar por email al cliente (si tiene email)
- Mostrar vista previa del PDF

#### 2.3. Generación de PDF

**Propósito:** Crear documento profesional para entregar al cliente.

**Estructura del PDF:**

**Página 1 - Portada:**
- Logo de la empresa (desde `empresa.logo`)
- Nombre de la empresa
- RIF
- Dirección, teléfono, email
- Título: "COTIZACIÓN" (grande, centrado)
- Número: COT-2024-001
- Fecha: DD/MM/YYYY

**Página 2 - Datos del cliente y proyecto:**
```
CLIENTE:
  Nombre: [cliente_nombre]
  RIF: [cliente_rif]
  Dirección: [cliente_direccion]
  Teléfono: [cliente_telefono]

PROYECTO:
  Nombre: [nombre_proyecto]
  Ubicación: [ubicacion]
  Descripción:
  [descripcion]
```

**Páginas siguientes - Partidas:**

Tabla agrupada por categoría:

```
CATEGORÍA: PRELIMINARES
┌────────┬──────────────────────────────┬────────┬──────────┬────────────┬────────────┐
│ Código │ Descripción                  │ Unidad │ Cantidad │ P. Unit.   │ Subtotal   │
├────────┼──────────────────────────────┼────────┼──────────┼────────────┼────────────┤
│ 01.01  │ Limpieza de terreno          │ m2     │   250.00 │ $    2.50  │ $   625.00 │
│ 01.02  │ Replanteo y nivelación       │ m2     │   250.00 │ $    1.80  │ $   450.00 │
├────────┴──────────────────────────────┴────────┴──────────┴────────────┼────────────┤
│                                          SUBTOTAL PRELIMINARES:         │ $ 1,075.00 │
└─────────────────────────────────────────────────────────────────────────┴────────────┘

CATEGORÍA: ESTRUCTURA
[... más partidas ...]
```

**Página final - Totales y términos:**

```
                                          SUBTOTAL: $ 10,500.00
                          Utilidad (15%): $  1,575.00
                        ═══════════════════════════════
                          TOTAL: $ 12,075.00


TÉRMINOS Y CONDICIONES:
[terminos_condiciones]


VALIDEZ: Esta cotización tiene validez hasta el DD/MM/YYYY


_________________________                    _________________________
   Firma del Cliente                         [Nombre Empresa]
                                              [RIF]
```

**Requisitos técnicos:**
- Biblioteca: ReportLab o WeasyPrint
- Formato: PDF/A (archivable)
- Tamaño: Carta (8.5" × 11")
- Márgenes: 2cm todos los lados
- Fuente: Sans-serif profesional (Helvetica/Arial)
- Colores: Usar paleta de la empresa si está definida

#### 2.4. Flujo de Estados

**Diagrama de transiciones:**

```
    [NUEVA]
      ↓
  BORRADOR ←→ (editar)
      ↓ (enviar)
   ENVIADA
      ↓
   ┌──┴──┐
   ↓     ↓
APROBADA RECHAZADA
   ↓
CONVERTIDA
(a proyecto)
```

**Validaciones de transición:**
- BORRADOR → ENVIADA: Requiere todas las partidas válidas
- ENVIADA → APROBADA: Solo usuarios con rol ADMIN/GERENTE
- APROBADA → CONVERTIDA: Crea proyecto automáticamente
- No se puede editar cotización en estado APROBADA, RECHAZADA o CONVERTIDA

#### 2.5. Convertir Cotización a Proyecto

**Proceso:**

1. Validar que cotización.estado = APROBADA
2. Crear nuevo `Proyecto`:
   - Copiar todos los datos de cliente y proyecto
   - `cotizacion_origen` = cotización actual
   - `valor_contrato` = cotización.total
   - `estado` = PLANIFICACION
   - `gerente_proyecto` = usuario actual
3. Crear `PartidaProyecto` por cada `PartidaCotizacion`:
   - Copiar: código, descripción, unidad, categoría
   - `cantidad_presupuestada` = cantidad
   - `precio_unitario_presupuestado` = precio_unitario
   - `costo_presupuestado` = subtotal
   - `cantidad_ejecutada` = 0
   - `costo_real` = 0
   - `estado` = NO_INICIADA
4. Cambiar `cotizacion.estado` = CONVERTIDA
5. Redirigir a vista de proyecto recién creado

---

### MÓDULO 3: Base de Datos de Costos

**URLs principales:**
- `/bd-costos/` - Lista de ítems
- `/bd-costos/nuevo/` - Crear ítem
- `/bd-costos/<id>/` - Ver detalle
- `/bd-costos/<id>/editar/` - Editar
- `/bd-costos/<id>/historial/` - Ver historial de precios
- `/bd-costos/categorias/` - Gestionar categorías
- `/bd-costos/importar/` - Importar desde Excel
- `/bd-costos/exportar/` - Exportar a Excel

#### 3.1. Vista de Lista

**Buscador inteligente:**
- Input de texto que busca en:
  - `codigo` (exacto o parcial)
  - `descripcion` (texto completo)
  - `especificaciones`
- Búsqueda con HTMX: resultados sin recargar página

**Filtros:**
- Tipo: Todos, Material, Mano de obra, Equipo, Subcontrato, Otros
- Categoría: Select jerárquico de categorías
- Activo: Sí, No, Todos
- Moneda: USD, VES, Todas

**Vista de tabla:**
```
┌────────┬──────────────────────────┬──────────┬────────┬───────────┬────────────┬──────────┐
│ Código │ Descripción              │ Tipo     │ Unidad │ Precio    │ Últ. Act.  │ Acciones │
├────────┼──────────────────────────┼──────────┼────────┼───────────┼────────────┼──────────┤
│MAT-001 │ Cemento Portland tipo I  │ Material │ saco   │ $ 8.50    │ 15/01/2024 │ [E][H][X]│
│MAT-002 │ Cabilla 1/2"             │ Material │ kg     │ $ 0.85    │ 10/01/2024 │ [E][H][X]│
│MO-010  │ Maestro de obra          │ M. Obra  │ día    │ $ 45.00   │ 20/12/2023 │ [E][H][X]│
└────────┴──────────────────────────┴──────────┴────────┴───────────┴────────────┴──────────┘
```
[E] = Editar, [H] = Historial, [X] = Desactivar

**Acciones rápidas:**
- Editar: Abrir modal con formulario
- Historial: Modal con gráfico de tendencia de precios
- Desactivar: Soft delete (activo = False)

#### 3.2. Crear/Editar Ítem

**Formulario:**

**Identificación:**
- Código: Input text (requerido, único por empresa)
  - Sugerencia de formato: TIPO-### (ej: MAT-001, MO-010)
  - Validar que no exista
- Descripción: Input text, largo (requerido, max 300 chars)
- Tipo: Select (requerido)
  - Material
  - Mano de Obra
  - Equipo/Maquinaria
  - Subcontrato
  - Otros

**Clasificación:**
- Categoría: Select jerárquico (opcional)
  - Mostrar jerarquía: "Estructura > Fundaciones"
  - Link rápido: "Crear nueva categoría"

**Medición:**
- Unidad: Select con opciones predefinidas + opción custom
  - Predefinidas: m2, m3, kg, ton, un, lote, ml, día, hora, mes
  - Custom: Input text si elige "Otra"

**Precio:**
- Precio actual: Input numérico (requerido, > 0)
- Moneda: Radio buttons (USD / VES)

**Detalles adicionales (opcional):**
- Especificaciones técnicas: Textarea
  - Ej: "Cemento portland tipo I, norma COVENIN 28"
- Proveedor preferido: Input text
- Notas internas: Textarea

**Validaciones:**
- Código único por empresa
- Precio > 0
- Descripción no vacía

**Al guardar:**
- Si es edición Y precio cambió:
  - Crear registro en `HistorialPrecio` con precio anterior
  - Actualizar `precio_actual` del ítem
  - Actualizar `fecha_actualizacion`

#### 3.3. Gestión de Categorías

**Vista de árbol jerárquico:**

```
📁 PRELIMINARES (01)
  📄 Limpieza de terreno (01.01)
  📄 Replanteo (01.02)
  📄 Excavaciones (01.03)
📁 ESTRUCTURA (02)
  📁 Fundaciones (02.01)
    📄 Zapatas (02.01.01)
    📄 Vigas de riostra (02.01.02)
  📄 Columnas (02.02)
  📄 Vigas (02.03)
📁 ALBAÑILERÍA (03)
  📄 Paredes (03.01)
  📄 Frisos (03.02)
```

**Acciones:**
- Agregar categoría raíz
- Agregar subcategoría bajo cualquier nodo
- Editar nombre/código
- Eliminar (solo si no tiene ítems asociados)
- Reordenar con drag & drop

**Formulario de categoría:**
- Nombre: Input text (requerido)
- Código: Input text (requerido, único)
- Padre: Select de categorías (opcional, null = raíz)
- Descripción: Textarea (opcional)

#### 3.4. Historial de Precios

**Modal que muestra:**

**Tabla histórica:**
```
┌────────────┬───────────┬─────────┬──────────────────────────┐
│ Fecha      │ Precio    │ Moneda  │ Observación              │
├────────────┼───────────┼─────────┼──────────────────────────┤
│ 15/01/2024 │ $  8.50   │ USD     │ Ajuste por inflación     │
│ 10/12/2023 │ $  8.20   │ USD     │ Precio inicial           │
│ 05/11/2023 │ $  8.00   │ USD     │ -                        │
└────────────┴───────────┴─────────┴──────────────────────────┘
```

**Gráfico de línea:**
- Eje X: Fechas
- Eje Y: Precio
- Mostrar tendencia (subida/bajada)
- Marcar precio actual con punto destacado

**Estadísticas:**
- Precio promedio (últimos 6 meses)
- Variación % (desde precio más antiguo)
- Última actualización hace X días

#### 3.5. Importar desde Excel

**Propósito:** Carga masiva inicial de ítems desde archivo Excel de Valmore.

[PENDIENTE - ¿Valmore tiene Excel con costos? ¿Qué columnas tiene?]

**Formato esperado del Excel:**

| Código  | Descripción              | Tipo      | Unidad | Precio | Moneda | Categoría  | Proveedor        |
|---------|--------------------------|-----------|--------|--------|--------|------------|------------------|
| MAT-001 | Cemento Portland tipo I  | Material  | saco   | 8.50   | USD    | Materiales | Cementos CA      |
| MAT-002 | Cabilla 1/2"             | Material  | kg     | 0.85   | USD    | Materiales | Ferretería Total |
| MO-010  | Maestro de obra          | Mano Obra | día    | 45.00  | USD    | -          | -                |

**Proceso:**
1. Usuario sube archivo .xlsx
2. Sistema valida:
   - Formato correcto (columnas esperadas)
   - Tipos de datos válidos
   - Códigos no duplicados con BD existente
3. Mostrar preview de filas a importar
4. Usuario confirma o cancela
5. Sistema crea ItemCosto por cada fila válida
6. Reporte final:
   - X ítems importados exitosamente
   - Y ítems con errores (mostrar cuáles y por qué)

**Manejo de errores:**
- Código duplicado: Skip fila, reportar
- Precio inválido: Skip fila, reportar
- Categoría no existe: Crear automáticamente o skip según opción
- Tipo no válido: Skip fila, reportar

#### 3.6. Exportar a Excel

**Propósito:** Respaldo o compartir BD de costos.

**Contenido del Excel:**
- Todas las columnas del modelo ItemCosto
- Filtrado según filtros activos en vista
- Incluir hoja adicional con categorías
- Nombre archivo: `BD_Costos_[Empresa]_[Fecha].xlsx`

**Formato:**
- Encabezados en negrita
- Columnas autoajustadas
- Precio con formato moneda
- Fecha en formato DD/MM/YYYY

---

### MÓDULO 4: Proyectos en Ejecución

**URLs principales:**
- `/proyectos/` - Lista de proyectos
- `/proyectos/<id>/` - Vista detallada
- `/proyectos/<id>/editar/` - Editar info básica
- `/proyectos/<id>/partida/<partida_id>/registrar-avance/` - Registrar avance
- `/proyectos/<id>/fotos/` - Galería de fotos
- `/proyectos/<id>/fotos/subir/` - Subir fotos
- `/proyectos/<id>/orden-cambio/nueva/` - Nueva orden de cambio
- `/proyectos/<id>/orden-cambio/<oc_id>/aprobar/` - Aprobar OC

#### 4.1. Lista de Proyectos

**Filtros:**
- Estado: Todos, Planificación, En Ejecución, Pausado, Completado, Cancelado
- Gerente: Todos, [lista de gerentes]
- Rango de fechas: Inicio planeado, Fin planeado
- Rentabilidad: Todos, Positiva, Negativa, Break-even

**Vista de cards (responsive):**

```
┌──────────────────────────────────────────────────────────────┐
│ PROY-2024-001 - Remodelación Oficina Central                │
│ Cliente: Inversiones XYZ, C.A.                               │
├──────────────────────────────────────────────────────────────┤
│ [████████░░] 80% Avance      🚨 Atrasado 3 días              │
├─────────────────┬─────────────────┬──────────────────────────┤
│ Valor: $45,000  │ Costo: $38,200  │ Utilidad: $6,800 (15.1%) │
│ Inicio: 15/01   │ Fin: 28/02      │ Gerente: [Nombre]        │
├──────────────────────────────────────────────────────────────┤
│ [Ver Detalle] [Registrar Avance] [Subir Fotos]              │
└──────────────────────────────────────────────────────────────┘
```

**Indicadores visuales:**
- Barra de progreso coloreada (verde >80%, amarillo 40-80%, rojo <40%)
- Badge de estado (EN_EJECUCION, PAUSADO, etc.)
- Alerta de retraso si está atrasado

#### 4.2. Vista Detallada de Proyecto

**Tabs principales:**

**Tab 1: Resumen**

**Header con stats:**
```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Avance       │ Valor        │ Costo Real   │ Rentabilidad │
│   [80%]      │ [$45,000]    │ [$38,200]    │   [15.1%]    │
│ ⭕ 80%      │              │              │ 🟢 Positivo  │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

**Información general:**
- Cliente, ubicación, descripción
- Fechas: Planeadas vs Reales
- Gerente, Supervisor
- Estado actual

**Cronología visual:**
```
[============|========>------] Hoy
Inicio Plan  Inicio Real   Fin Plan
15/01/24     18/01/24      28/02/24
```

**Tab 2: Partidas**

**Tabla detallada:**
```
┌──────┬────────────────────┬──────┬──────────┬──────────┬────────┬───────────┬───────────┬──────────┬────────┬──────────┐
│ Cód. │ Descripción        │ Und. │ Cant.Pre │ Cant.Eje │ %Av    │ Costo Pre │ Costo Rea │ Variación│ Estado │ Acciones │
├──────┼────────────────────┼──────┼──────────┼──────────┼────────┼───────────┼───────────┼──────────┼────────┼──────────┤
│01.01 │Limpieza terreno    │ m2   │   250.00 │   250.00 │ 100%   │ $  625.00 │ $  610.00 │ -2.4% 🟢 │Completa│ [Ver]    │
│01.02 │Replanteo           │ m2   │   250.00 │   200.00 │  80%   │ $  450.00 │ $  380.00 │ -15.6%🟢│En Proc │ [+Avance]│
│02.01 │Excavación manual   │ m3   │    45.00 │    30.00 │  67%   │ $  540.00 │ $  420.00 │ -22.2%🟢│En Proc │ [+Avance]│
└──────┴────────────────────┴──────┴──────────┴──────────┴────────┴───────────┴───────────┴──────────┴────────┴──────────┘
```

**Indicadores de variación:**
- 🟢 Verde: Costo real < presupuestado (ahorro)
- 🔴 Rojo: Costo real > presupuestado (sobrecosto)
- % de variación claramente visible

**Acción: Registrar Avance**
Abre modal con formulario (ver sección 4.3)

**Tab 3: Cronograma** [OPCIONAL EN MVP - Depende de complejidad]

Opciones:
- **Opción simple:** Tabla con fechas planificadas por partida
- **Opción completa:** Gráfico Gantt interactivo (requiere biblioteca JS)

[PENDIENTE - Confirmar con Valmore: ¿Necesita Gantt o tabla simple es suficiente?]

**Tab 4: Fotos**

**Galería de imágenes:**
```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ [IMG]        │ [IMG]        │ [IMG]        │ [IMG]        │
│ Estructura   │ Acabados     │ Instalaciones│ Fachada      │
│ 15/01/2024   │ 22/01/2024   │ 05/02/2024   │ 12/02/2024   │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

**Funcionalidades:**
- Subir múltiples fotos a la vez
- Ver en lightbox al hacer click
- Ordenar por fecha (más recientes primero)
- Descripción debajo de cada foto
- Botón: "Subir Fotos"

**Restricciones:**
- Máximo 10 fotos por carga
- Formatos: JPG, PNG
- Tamaño máximo: 5MB por foto
- Se comprimen automáticamente a 1920px ancho

**Tab 5: Órdenes de Cambio**

**Lista de órdenes:**
```
┌────────┬─────────────────────────┬──────────────┬───────────────┬──────────┬──────────┐
│ N°     │ Descripción             │ Impacto $    │ Impacto Días  │ Estado   │ Acciones │
├────────┼─────────────────────────┼──────────────┼───────────────┼──────────┼──────────┤
│ OC-001 │ Cambio de piso cerámico │ + $2,500.00  │ + 5 días      │ Aprobada │ [Ver]    │
│ OC-002 │ Instalación adicional   │ + $1,200.00  │ + 2 días      │ Pendiente│ [Aprobar]│
└────────┴─────────────────────────┴──────────────┴───────────────┴──────────┴──────────┘
```

**Botón:** "Nueva Orden de Cambio"

**Tab 6: Equipo** [OPCIONAL]

Lista de usuarios asignados al proyecto:
- Gerente (1)
- Supervisor (1 o más)
- Otros roles custom si aplican

#### 4.3. Registrar Avance de Partida

**Modal/Formulario:**

```
┌─────────────────────────────────────────────────────────────┐
│ Registrar Avance - Excavación Manual                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Partida: 02.01 - Excavación manual                          │
│ Unidad: m3                                                   │
│ Presupuestado: 45.00 m3                                      │
│ Ejecutado anterior: 30.00 m3                                 │
│ Restante: 15.00 m3                                           │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Fecha: [___________] (default: hoy)                          │
│                                                              │
│ Cantidad ejecutada hoy: [___________] m3                     │
│                                                              │
│ Costo real del día: $[___________]                           │
│                                                              │
│ Observaciones:                                               │
│ [________________________________________________]           │
│ [________________________________________________]           │
│ [________________________________________________]           │
│                                                              │
│        [Cancelar]              [Guardar Registro]            │
└─────────────────────────────────────────────────────────────┘
```

**Validaciones:**
- Fecha no puede ser futura
- Cantidad ejecutada > 0
- Costo real > 0
- Observaciones opcionales pero recomendadas

**Al guardar:**
1. Crear `RegistroAvance` (inmutable)
2. Actualizar `PartidaProyecto`:
   - `cantidad_ejecutada += cantidad_ejecutada_dia`
   - `costo_real += costo_dia`
   - Recalcular `porcentaje_avance`
   - Actualizar `estado` si corresponde
3. Recalcular `Proyecto.porcentaje_avance`:
   - Promedio ponderado de avances de partidas (por costo presupuestado)
4. Mostrar mensaje de éxito
5. Refrescar tabla de partidas con HTMX

#### 4.4. Gestión de Órdenes de Cambio

**Crear Nueva Orden de Cambio:**

**Formulario:**
```
Descripción del cambio:
[__________________________________________________________________]

Justificación:
[__________________________________________________________________]
[__________________________________________________________________]

Impacto en costo: $[___________] (positivo o negativo)
Impacto en tiempo: [_____] días (positivo o negativo)

        [Cancelar]              [Solicitar Aprobación]
```

**Al crear:**
- Estado inicial = PENDIENTE
- `solicitado_por` = usuario actual
- Número secuencial dentro del proyecto

**Aprobar/Rechazar Orden de Cambio:**

Modal de aprobación:
```
┌─────────────────────────────────────────────────────────────┐
│ Orden de Cambio OC-002                                       │
├─────────────────────────────────────────────────────────────┤
│ Descripción: [mostrar descripción]                           │
│ Justificación: [mostrar justificación]                       │
│ Impacto Costo: + $1,200.00                                   │
│ Impacto Tiempo: + 2 días                                     │
│ Solicitado por: [Nombre] el DD/MM/YYYY                       │
├─────────────────────────────────────────────────────────────┤
│ Observaciones de aprobación:                                 │
│ [________________________________________________]           │
│                                                              │
│      [Rechazar]      [Aprobar]                               │
└─────────────────────────────────────────────────────────────┘
```

**Solo usuarios ADMIN o GERENTE pueden aprobar.**

**Al aprobar:**
- Cambiar estado = APROBADA
- Registrar fecha_aprobacion
- Si impacto_costo > 0: `proyecto.valor_contrato += impacto_costo`
- Si impacto_tiempo_dias != 0: `proyecto.fecha_fin_planeada += days(impacto_tiempo_dias)`

**Al rechazar:**
- Cambiar estado = RECHAZADA
- No modificar proyecto
- Registrar observaciones

---

### MÓDULO 5: Reportes

**URLs principales:**
- `/reportes/` - Dashboard de reportes
- `/reportes/rentabilidad-proyecto/` - Reporte de rentabilidad
- `/reportes/flujo-caja/` - Proyección de flujo
- `/reportes/analisis-cotizaciones/` - Métricas de cotizaciones
- `/reportes/costos-categoria/` - Distribución de costos

#### 5.1. Dashboard de Reportes

**Selector de reporte:**
- Dropdown con opciones de reportes disponibles
- Filtros comunes:
  - Rango de fechas (desde - hasta)
  - Proyecto específico (opcional)
  - Estado de proyectos (todos, activos, completados)

**Botones de acción:**
- [Generar Reporte] - Muestra en pantalla con HTMX
- [Exportar a Excel] - Descarga archivo .xlsx
- [Exportar a PDF] - Descarga PDF del reporte

#### 5.2. Reporte: Rentabilidad por Proyecto

**Tabla principal:**
```
┌─────────────────┬─────────────┬─────────────┬─────────────┬──────────┬───────────────┐
│ Proyecto        │ Valor       │ Costo Real  │ Utilidad    │ Margen % │ Estado        │
├─────────────────┼─────────────┼─────────────┼─────────────┼──────────┼───────────────┤
│ PROY-2024-001   │ $ 45,000.00 │ $ 38,200.00 │ $ 6,800.00  │  15.1%   │ En Ejecución  │
│ PROY-2024-002   │ $ 32,500.00 │ $ 28,100.00 │ $ 4,400.00  │  13.5%   │ Completado    │
│ PROY-2023-015   │ $ 28,000.00 │ $ 29,500.00 │ $(1,500.00) │  -5.4%🔴│ Completado    │
├─────────────────┼─────────────┼─────────────┼─────────────┼──────────┼───────────────┤
│ TOTAL           │ $105,500.00 │ $ 95,800.00 │ $ 9,700.00  │   9.2%   │               │
└─────────────────┴─────────────┴─────────────┴─────────────┴──────────┴───────────────┘
```

**Gráfico de barras:**
- Eje X: Proyectos (nombres)
- Eje Y: Monto ($)
- Barras agrupadas:
  - Azul: Valor contrato
  - Rojo: Costo real
  - Verde: Utilidad

**Métricas resumen:**
- Total facturado (suma valores contratos)
- Total de costos (suma costos reales)
- Utilidad total
- Margen promedio (utilidad/facturado × 100)
- Proyectos con utilidad positiva vs negativa

#### 5.3. Reporte: Análisis de Cotizaciones

**Propósito:** Métricas de efectividad comercial.

**KPIs principales:**
```
┌─────────────────────┬─────────────────────┬─────────────────────┐
│ Tasa de Conversión  │ Tiempo Promedio     │ Valor Promedio      │
│       45.5%         │  Respuesta          │  Cotización         │
│ (10 de 22)          │     7.2 días        │    $35,250          │
└─────────────────────┴─────────────────────┴─────────────────────┘
```

**Cálculos:**
- **Tasa de conversión:** (cotizaciones APROBADAS / total cotizaciones ENVIADAS) × 100
- **Tiempo promedio respuesta:** PROMEDIO de (fecha_respuesta - fecha_envio) para cotizaciones respondidas
- **Valor promedio:** PROMEDIO de cotizacion.total para todas las cotizaciones

**Tabla por estado:**
```
┌─────────────────┬──────────┬────────────┬─────────────────┐
│ Estado          │ Cantidad │ Valor Total│ % del Total     │
├─────────────────┼──────────┼────────────┼─────────────────┤
│ Aprobadas       │    10    │ $352,500   │     45.5%       │
│ Rechazadas      │     5    │ $186,300   │     22.7%       │
│ Pendientes      │     7    │ $210,800   │     31.8%       │
└─────────────────┴──────────┴────────────┴─────────────────┘
```

**Gráfico de pie:**
- Distribución por estado
- Colores: Verde (Aprobadas), Rojo (Rechazadas), Amarillo (Pendientes)

**Tendencia temporal:**
- Gráfico de línea: Cotizaciones enviadas por mes (últimos 12 meses)

#### 5.4. Reporte: Costos por Categoría

**Propósito:** Ver distribución de costos por tipo/categoría.

**Gráfico de dona:**
- Materiales: 45%
- Mano de Obra: 30%
- Equipos: 15%
- Subcontratos: 8%
- Otros: 2%

**Tabla detallada:**
```
┌─────────────────┬─────────────┬───────────────┬───────────────────┐
│ Categoría       │ Costo Total │ % del Total   │ Proyectos         │
├─────────────────┼─────────────┼───────────────┼───────────────────┤
│ Materiales      │ $ 43,110.00 │    45.0%      │ 8 proyectos       │
│ Mano de Obra    │ $ 28,740.00 │    30.0%      │ 8 proyectos       │
│ Equipos         │ $ 14,370.00 │    15.0%      │ 5 proyectos       │
│ Subcontratos    │ $  7,664.00 │     8.0%      │ 3 proyectos       │
│ Otros           │ $  1,916.00 │     2.0%      │ 2 proyectos       │
├─────────────────┼─────────────┼───────────────┼───────────────────┤
│ TOTAL           │ $ 95,800.00 │   100.0%      │                   │
└─────────────────┴─────────────┴───────────────┴───────────────────┘
```

**Análisis por proyecto:**
- Permitir seleccionar proyecto específico
- Ver distribución de costos de ese proyecto
- Comparar con promedios generales

#### 5.5. Exportación a Excel

**Contenido del archivo:**
- **Hoja 1:** Datos tabulados del reporte
- **Hoja 2:** Gráficos (si aplica)
- **Hoja 3:** Metadata (fecha de generación, filtros aplicados, usuario)

**Formato:**
- Encabezados en negrita, color de fondo
- Totales en negrita
- Números formateados (moneda, porcentajes)
- Colores condicionales (verde/rojo según valores positivos/negativos)

---

## 👥 SISTEMA DE ROLES Y PERMISOS

### Matriz de Permisos

| Funcionalidad                        | ADMIN | GERENTE | SUPERVISOR | CLIENTE |
|--------------------------------------|-------|---------|------------|---------|
| **Dashboard**                        |       |         |            |         |
| Ver dashboard principal              | ✅     | ✅       | ✅          | ❌       |
| Ver KPIs globales                    | ✅     | ✅       | Solo asign.| ❌       |
| **Cotizaciones**                     |       |         |            |         |
| Ver todas las cotizaciones           | ✅     | ✅       | ❌          | Solo propias|
| Crear cotización                     | ✅     | ✅       | ❌          | ❌       |
| Editar cotización                    | ✅     | ✅       | ❌          | ❌       |
| Eliminar cotización                  | ✅     | ❌       | ❌          | ❌       |
| Aprobar/Rechazar cotización          | ✅     | ✅       | ❌          | ❌       |
| Convertir a proyecto                 | ✅     | ✅       | ❌          | ❌       |
| Descargar PDF                        | ✅     | ✅       | ✅          | Solo propias|
| **BD de Costos**                     |       |         |            |         |
| Ver ítems                            | ✅     | ✅       | Solo lectura| ❌       |
| Crear/Editar ítems                   | ✅     | ✅       | ❌          | ❌       |
| Eliminar ítems                       | ✅     | ❌       | ❌          | ❌       |
| Importar/Exportar                    | ✅     | ✅       | ❌          | ❌       |
| Gestionar categorías                 | ✅     | ✅       | ❌          | ❌       |
| **Proyectos**                        |       |         |            |         |
| Ver todos los proyectos              | ✅     | ✅       | Solo asign.| Solo propios|
| Crear proyecto                       | ✅     | ✅       | ❌          | ❌       |
| Editar proyecto                      | ✅     | ✅       | ❌          | ❌       |
| Eliminar proyecto                    | ✅     | ❌       | ❌          | ❌       |
| Registrar avance                     | ✅     | ✅       | ✅ (asign.) | ❌       |
| Subir fotos                          | ✅     | ✅       | ✅ (asign.) | ❌       |
| Ver fotos                            | ✅     | ✅       | ✅          | Solo propios|
| Crear orden de cambio                | ✅     | ✅       | ✅ (asign.) | ❌       |
| Aprobar orden de cambio              | ✅     | ✅       | ❌          | ❌       |
| **Reportes**                         |       |         |            |         |
| Ver todos los reportes               | ✅     | ✅       | ❌          | ❌       |
| Exportar reportes                    | ✅     | ✅       | ❌          | ❌       |
| **Configuración**                    |       |         |            |         |
| Gestionar usuarios                   | ✅     | ❌       | ❌          | ❌       |
| Configurar empresa                   | ✅     | ❌       | ❌          | ❌       |
| Ver logs de auditoría                | ✅     | ❌       | ❌          | ❌       |

### Reglas Especiales de Permisos

**SUPERVISOR:**
- Solo ve proyectos donde está asignado como `supervisor`
- Puede registrar avances y subir fotos SOLO en esos proyectos
- No puede editar información del proyecto ni partidas presupuestadas
- No puede crear órdenes de cambio (solo solicitar informalmente)

**CLIENTE (acceso externo):**
- Usuario especial creado por ADMIN/GERENTE
- Asociado a cotización(es) o proyecto(s) específico(s)
- Solo ve información de SUS proyectos/cotizaciones
- Vista simplificada (sin información de costos reales internos)
- No puede hacer ninguna modificación
- Puede descargar PDFs de sus cotizaciones y reportes de avance

### Implementación de Permisos

**Decoradores personalizados:**
```
@requiere_rol('ADMIN', 'GERENTE')
def crear_cotizacion(request):
    # Solo ADMIN y GERENTE pueden acceder
    ...

@requiere_rol('ADMIN', 'GERENTE', 'SUPERVISOR')
@requiere_proyecto_asignado()
def registrar_avance(request, proyecto_id, partida_id):
    # SUPERVISOR solo si está asignado al proyecto
    ...
```

**Validaciones a nivel de QuerySet:**
```
# Proyectos visibles según rol
if request.user.rol == 'SUPERVISOR':
    proyectos = Proyecto.objects.filter(
        empresa=request.tenant,
        supervisor=request.user
    )
elif request.user.rol in ['ADMIN', 'GERENTE']:
    proyectos = Proyecto.objects.filter(empresa=request.tenant)
```

---

## 🎨 DISEÑO DE INTERFAZ DE USUARIO

### Paleta de Colores (Fondo Claro)

```css
/* Colores principales */
--primary: #2563eb;           /* Azul vibrante (botones principales, links) */
--primary-dark: #1e40af;      /* Azul oscuro (hover) */
--secondary: #10b981;         /* Verde esmeralda (éxito, completado) */
--accent: #f59e0b;            /* Ámbar (alertas, pendiente) */
--danger: #ef4444;            /* Rojo (errores, eliminación) */

/* Fondos - TEMA CLARO */
--bg-primary: #ffffff;        /* Fondo principal blanco */
--bg-secondary: #f8fafc;      /* Fondo secundario gris muy claro */
--bg-tertiary: #f1f5f9;       /* Fondo tarjetas gris claro */

/* Textos - OPTIMIZADOS PARA FONDO CLARO */
--text-primary: #0f172a;      /* Texto principal negro azulado */
--text-secondary: #475569;    /* Texto secundario gris oscuro */
--text-tertiary: #94a3b8;     /* Texto terciario gris medio */

/* Bordes */
--border-light: #e2e8f0;      /* Bordes sutiles */
--border-medium: #cbd5e1;     /* Bordes normales */
--border-dark: #94a3b8;       /* Bordes enfatizados */

/* Sombras */
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
```

### Componentes UI Base

**Botones:**
- Primario: Fondo azul, texto blanco, bordes redondeados (8px)
- Secundario: Fondo verde, texto blanco
- Peligro: Fondo rojo, texto blanco
- Outline: Borde color, fondo transparente
- Tamaños: sm (32px alto), md (40px), lg (48px)

**Cards:**
- Fondo blanco/gris claro
- Borde sutil
- Sombra suave
- Padding: 24px
- Border-radius: 12px

**Tablas:**
- Header con fondo gris claro
- Filas alternadas (zebra striping)
- Hover efecto sutil
- Bordes horizontales sutiles

**Forms:**
- Labels en negrita, color texto primario
- Inputs con borde gris, fondo blanco
- Focus: Borde azul, sombra azul suave
- Error: Borde rojo, mensaje rojo debajo

**Modals:**
- Overlay semi-transparente (bg-black/50)
- Modal centrado con sombra grande
- Header con título y botón X
- Footer con acciones (Cancelar/Aceptar)

**Badges:**
- Pills con bordes redondeados
- Colores según estado:
  - Verde: Aprobado, Completado, Activo
  - Amarillo: Pendiente, En Proceso
  - Rojo: Rechazado, Cancelado, Atrasado
  - Gris: Borrador, Inactivo

### Navegación Principal

**Sidebar izquierdo:**
```
┌─────────────────────────┐
│ [Logo] Smart PM         │
├─────────────────────────┤
│ 📊 Dashboard            │
│ 📋 Cotizaciones         │
│ 💰 BD de Costos         │
│ 🏗️  Proyectos           │
│ 📈 Reportes             │
├─────────────────────────┤
│ ⚙️  Configuración       │ (solo ADMIN)
│ 👤 Mi Perfil            │
│ 🚪 Salir                │
└─────────────────────────┘
```

**Navbar superior:**
```
┌──────────────────────────────────────────────────────────────┐
│ [≡ Menu] Smart Project Management    [🔔] [Usuario ▼] [Salir]│
└──────────────────────────────────────────────────────────────┘
```

**Breadcrumbs:**
```
Dashboard > Proyectos > PROY-2024-001 > Partidas
```

### Responsive Breakpoints

**Mobile (< 768px):**
- Sidebar oculto por default (hamburger menu)
- Tablas con scroll horizontal
- Cards apiladas verticalmente
- Formularios 1 columna

**Tablet (768px - 1024px):**
- Sidebar colapsable
- Tablas responsivas
- Cards en grid 2 columnas

**Desktop (> 1024px):**
- Sidebar visible siempre
- Layout completo
- Cards en grid 3-4 columnas

---

## 🔄 FLUJOS DE USUARIO CRÍTICOS

### Flujo 1: Crear Cotización y Convertir a Proyecto

**Actores:** Gerente de proyecto (Valmore)

**Precondiciones:**
- BD de costos tiene ítems relevantes
- Usuario autenticado con rol GERENTE o ADMIN

**Pasos:**

1. **Crear cotización**
   - Usuario va a `/cotizaciones/nueva/`
   - Llena datos del cliente (nombre, teléfono, dirección)
   - Llena datos del proyecto (nombre, descripción, ubicación)
   - Define fecha de vencimiento (default: +15 días)

2. **Agregar partidas**
   - Click "Agregar desde BD de Costos"
   - Modal con buscador
   - Busca "cemento" → Selecciona "Cemento Portland"
   - Ajusta cantidad (ej: 50 sacos)
   - Sistema calcula subtotal automáticamente
   - Repite para otras partidas (cabilla, arena, mano de obra, etc.)
   - O agrega partidas manuales si no están en BD

3. **Revisar y ajustar**
   - Sistema muestra subtotal automático
   - Ajusta margen de utilidad si es necesario (default: 15%)
   - Revisa total calculado
   - Añade términos y condiciones
   - Agrega notas internas

4. **Guardar y enviar**
   - Opción A: "Guardar como Borrador" (puede editar después)
   - Opción B: "Generar y Enviar"
     - Sistema valida que todo esté completo
     - Genera PDF automáticamente
     - Cambia estado a ENVIADA
     - Usuario descarga PDF
     - [Opcional] Sistema envía email al cliente

5. **Cliente responde**
   - Usuario recibe respuesta del cliente (por teléfono/email)
   - Entra a cotización
   - Click "Marcar como Aprobada" o "Marcar como Rechazada"
   - Si aprobada: Botón "Convertir a Proyecto" se habilita

6. **Convertir a proyecto**
   - Click "Convertir a Proyecto"
   - Sistema crea proyecto automáticamente:
     - Copia datos de cliente y proyecto
     - Copia todas las partidas como presupuesto
     - Asigna gerente (usuario actual)
   - Usuario define:
     - Fecha de inicio planeada
     - Fecha de fin planeada
     - Supervisor (si aplica)
   - Sistema redirige a vista de proyecto nuevo

**Postcondiciones:**
- Cotización en estado CONVERTIDA
- Proyecto creado en estado PLANIFICACION
- Todas las partidas presupuestadas listas

---

### Flujo 2: Registrar Avance Diario de Proyecto

**Actores:** Supervisor de obra

**Precondiciones:**
- Proyecto existe y está en estado EN_EJECUCION
- Supervisor asignado al proyecto
- Usuario autenticado con rol SUPERVISOR

**Pasos:**

1. **Acceder al proyecto**
   - Supervisor va a `/proyectos/`
   - Ve solo proyectos donde está asignado
   - Click en proyecto "Remodelación Oficina XYZ"

2. **Ver partidas**
   - Tab "Partidas"
   - Ve lista de partidas con estado de avance
   - Identifica partida actual: "02.01 - Excavación manual"
   - Estado: En Proceso (67% completado)

3. **Registrar avance del día**
   - Click botón "Registrar Avance" en fila de partida
   - Modal se abre con formulario
   - Ve resumen:
     - Presupuestado: 45.00 m3
     - Ejecutado anterior: 30.00 m3
     - Restante: 15.00 m3

4. **Llenar datos del día**
   - Fecha: [hoy, autocompletado]
   - Cantidad ejecutada hoy: 8.00 m3
   - Costo real del día: $180.00
   - Observaciones: "Terreno más rocoso de lo previsto, requirió martillo neumático"

5. **Guardar registro**
   - Click "Guardar Registro"
   - Sistema valida datos
   - Crea RegistroAvance (inmutable)
   - Actualiza automáticamente:
     - cantidad_ejecutada = 30 + 8 = 38.00 m3
     - costo_real = $420 + $180 = $600
     - porcentaje_avance = (38/45) × 100 = 84.4%
     - Estado cambia a "En Proceso" si no estaba
   - Recalcula porcentaje de avance del proyecto completo

6. **Confirmación**
   - Modal se cierra
   - Tabla de partidas se actualiza automáticamente (HTMX)
   - Muestra nuevo estado de la partida
   - Supervisor puede ver cambio inmediato

7. **Subir foto del avance (opcional)**
   - Tab "Fotos"
   - Click "Subir Fotos"
   - Selecciona foto desde celular
   - Añade descripción: "Avance excavación - área norte"
   - Sistema sube y muestra en galería

**Postcondiciones:**
- RegistroAvance creado
- Partida actualizada
- Proyecto recalculado
- Foto asociada al proyecto (si se subió)

---

### Flujo 3: Generar Reporte de Rentabilidad

**Actores:** Gerente o Admin

**Precondiciones:**
- Existen proyectos con datos de ejecución
- Usuario autenticado con rol GERENTE o ADMIN

**Pasos:**

1. **Acceder a reportes**
   - Usuario va a `/reportes/`
   - Ve dashboard de reportes

2. **Seleccionar tipo de reporte**
   - Dropdown: Selecciona "Rentabilidad por Proyecto"
   - Define filtros:
     - Rango de fechas: 01/01/2024 - 31/12/2024
     - Estado: "Todos"

3. **Generar reporte**
   - Click "Generar Reporte"
   - Sistema calcula:
     - Para cada proyecto en el rango:
       - Valor contrato
       - Costo real (suma de costos de partidas)
       - Utilidad = Valor - Costo
       - Margen % = (Utilidad / Valor) × 100
     - Totales generales
     - Margen promedio

4. **Visualizar resultados**
   - Tabla con todos los proyectos
   - Filas coloreadas según rentabilidad:
     - Verde: Margen > 10%
     - Amarillo: Margen 0-10%
     - Rojo: Margen negativo
   - Gráfico de barras comparando valor vs costo
   - KPIs en la parte superior

5. **Analizar proyecto específico**
   - Click en fila de proyecto con rentabilidad negativa
   - Sistema abre detalle
   - Muestra partidas con mayor variación de costo
   - Identifica causas de sobrecosto

6. **Exportar reporte**
   - Click "Exportar a Excel"
   - Sistema genera archivo .xlsx
   - Incluye:
     - Hoja 1: Tabla de datos
     - Hoja 2: Gráficos
     - Hoja 3: Metadata
   - Usuario descarga archivo

7. **Tomar decisiones**
   - Con la información, gerente identifica:
     - Proyectos rentables (replicar estrategia)
     - Proyectos con pérdidas (ajustar procesos)
     - Partidas problemáticas (revisar presupuestos futuros)

**Postcondiciones:**
- Reporte generado y visualizado
- Archivo Excel descargado
- Insights documentados para mejora continua

---

## ⚙️ REQUISITOS NO FUNCIONALES

### Performance

**Tiempos de respuesta objetivo:**
- Carga inicial del dashboard: < 2 segundos
- Carga de vistas internas: < 1 segundo
- Búsqueda de ítems en BD costos: < 500ms
- Generación de PDF: < 5 segundos
- Carga de reporte con gráficos: < 3 segundos
- Acciones HTMX (agregar partida, etc.): < 300ms

**Optimizaciones requeridas:**
- Paginación en listas largas (20-50 items por página)
- Lazy loading de imágenes en galería
- Índices en base de datos para queries frecuentes
- Caching de reportes frecuentes (opcional en MVP)

### Escalabilidad

**Capacidad objetivo (por empresa):**
- Hasta 100 proyectos simultáneos
- Hasta 500 cotizaciones/año
- Hasta 1,000 ítems en BD de costos
- Hasta 10,000 registros de avance/proyecto
- Hasta 20 usuarios concurrentes

**Límites técnicos:**
- Tamaño máximo de foto: 5MB
- Máximo 10 fotos por carga
- Máximo 100 partidas por cotización (advertencia si excede)
- Máximo 50 órdenes de cambio por proyecto

### Seguridad

**Autenticación:**
- Passwords hasheados con algoritmo seguro (bcrypt/PBKDF2)
- Longitud mínima: 8 caracteres
- Debe incluir: mayúsculas, minúsculas, números
- Sesiones con timeout (24 horas de inactividad)

**Autorización:**
- Validación de permisos en cada vista
- Validación de pertenencia a empresa en queries
- No exponer IDs predecibles en URLs (usar UUIDs o slugs)
- CSRF protection habilitado

**Datos sensibles:**
- Información de costos solo visible para roles apropiados
- No exponer precios internos a clientes externos
- Logs de auditoría para cambios críticos (aprobaciones, cambios de estado)

**Configuraciones Django:**
- DEBUG = False en producción
- SECRET_KEY complejo y aleatorio
- ALLOWED_HOSTS configurado apropiadamente
- HTTPS obligatorio en producción
- Headers de seguridad (X-Frame-Options, CSP, etc.)

### Disponibilidad

**Objetivo:** 99.5% uptime (aprox. 3.6 horas downtime/mes)

**Respaldos:**
- Backup automático de base de datos: Diario
- Retención: 30 días
- Backup de archivos (fotos, logos): Semanal
- Procedimiento de restauración documentado

**Monitoreo:**
- Logs de errores centralizados
- Alertas de errores críticos (500, database down)
- Monitoreo de uso de recursos (CPU, RAM, disco)

### Usabilidad

**Principios:**
- Interfaz intuitiva, mínimo entrenamiento requerido
- Mensajes de error claros y accionables
- Feedback inmediato en acciones del usuario
- Confirmaciones en acciones destructivas
- Ayuda contextual donde sea necesario

**Accesibilidad:**
- Contraste suficiente en textos (WCAG AA mínimo)
- Navegación por teclado funcional
- Labels descriptivos en forms
- Alt text en imágenes relevantes

### Compatibilidad

**Navegadores soportados:**
- Chrome/Edge (últimas 2 versiones)
- Firefox (últimas 2 versiones)
- Safari (últimas 2 versiones)

**Dispositivos:**
- Desktop: 1920×1080 y superiores (óptimo)
- Desktop: 1366×768 (funcional)
- Tablet: 768px ancho (funcional)
- Mobile: 375px ancho (funcional básico)

**Sistema operativo:**
- Windows 10/11
- macOS 11+
- iOS 14+
- Android 10+

---

## ❓ INFORMACIÓN FALTANTE Y PREGUNTAS PENDIENTES

### 🔴 CRÍTICO - Necesario antes de iniciar desarrollo

**Sobre el cliente Valmore:**

1. **Nombre legal de la empresa**
   - ¿Razón social registrada?
   - ¿RIF?
   - ¿Nombre comercial?

2. **Logo y marca**
   - ¿Tiene logo?
   - ¿Puede compartirlo? (formato vectorial ideal)
   - ¿Colores corporativos específicos?

3. **Estructura de costos actual**
   - ¿Tiene Excel con costos? ¿Puede compartirlo?
   - ¿Qué columnas tiene ese Excel?
   - ¿Cuántos ítems aproximadamente?
   - ¿Está actualizado?

4. **Volúmenes de operación**
   - ¿Cuántas cotizaciones genera por mes?
   - ¿Cuántos proyectos simultáneos maneja?
   - ¿Cuántos proyectos completa por año?
   - ¿Valor típico de un proyecto?

5. **Equipo de trabajo**
   - ¿Cuántas personas necesitan acceso?
   - ¿Qué roles tienen? (gerente, supervisor, administrativo)
   - ¿Quién creará cotizaciones?
   - ¿Quién registrará avances?

### 🟡 IMPORTANTE - Afecta diseño de funcionalidades

**Procesos de negocio:**

6. **Flujo de cotización a proyecto**
   - Cuando cliente aprueba: ¿Se firma contrato formal?
   - ¿Requiere anticipo? ¿Qué porcentaje?
   - ¿Cómo se formaliza? ¿Necesita registro digital en el sistema?

7. **Seguimiento de avance**
   - ¿Con qué frecuencia registra avances? ¿Diario? ¿Semanal?
   - ¿Quién lo hace? ¿Supervisor? ¿Maestro de obra?
   - ¿Desde dónde? ¿Obra? ¿Oficina?

8. **Órdenes de cambio**
   - ¿Maneja órdenes de cambio formalmente?
   - ¿Cómo las aprueba actualmente?
   - ¿Necesita firma del cliente digital?

9. **Control de inventario**
   - ¿Necesita control de materiales en bodega?
   - ¿O solo registra costos cuando se usan?

10. **Proveedores**
    - ¿Necesita módulo de proveedores separado?
    - ¿O basta con campo "proveedor preferido" en cada ítem?

### 🟢 DESEABLE - Para optimizar UX

**Preferencias de interfaz:**

11. **Términos y condiciones**
    - ¿Puede compartir T&C típicos de sus cotizaciones?
    - Para pre-cargar como default

12. **Formato de cotización**
    - ¿Tiene ejemplo de cotización actual que le guste?
    - ¿Puede compartirlo para replicar formato?

13. **Estructura de categorías**
    - ¿Cómo organiza sus partidas?
    - ¿Tiene nomenclatura estándar? (Ej: APU venezolanas)

14. **Unidades de medida**
    - ¿Qué unidades usa más frecuentemente?
    - Para crear presets en selects

15. **Moneda principal**
    - ¿Trabaja principalmente en USD o VES?
    - ¿O mixto según cliente?

### 🔵 OPCIONAL - Para fases futuras

**Funcionalidades adicionales:**

16. **Cronograma Gantt**
    - ¿Necesita cronograma Gantt interactivo?
    - ¿O basta con fechas inicio/fin por partida?

17. **Facturación fiscal**
    - ¿Necesita emitir facturas fiscales desde el sistema?
    - (Nota: requiere homologación SENIAT, fuera de MVP)

18. **Portal de cliente**
    - ¿Le gustaría que sus clientes puedan entrar al sistema?
    - ¿Para ver avance de su proyecto en tiempo real?

19. **Notificaciones automáticas**
    - ¿Quiere recibir alertas por email?
    - ¿Qué eventos? (proyecto atrasado, cotización sin respuesta, etc.)

20. **Integración contabilidad**
    - ¿Usa software de contabilidad? ¿Cuál?
    - ¿Necesita exportar datos para contabilidad?

---

## ✅ CRITERIOS DE ÉXITO

### Criterios Funcionales

**MVP será exitoso si:**

1. **Valmore puede crear cotización completa en < 5 minutos**
   - Desde abrir pantalla hasta generar PDF
   - Incluyendo agregar 10-15 partidas desde BD

2. **BD de costos está centralizada y actualizada**
   - Mínimo 100 ítems cargados
   - Búsqueda encuentra ítems en < 1 segundo
   - Historial de precios funcionando

3. **Puede hacer seguimiento diario de proyectos**
   - Registrar avance en < 2 minutos
   - Ver % de avance actualizado inmediatamente
   - Identificar variaciones de costo fácilmente

4. **Genera reportes automáticos útiles**
   - Rentabilidad por proyecto clara
   - Export a Excel funcional
   - Datos correctos vs cálculo manual

5. **100% de cotizaciones sin usar Excel**
   - Después de 1 mes de uso
   - Valmore confirma que no necesita Excel para cotizar

### Criterios Técnicos

**MVP será exitoso si:**

1. **Sistema es estable**
   - Zero errores 500 en 1 mes de uso
   - Todas las vistas cargan correctamente
   - No hay pérdida de datos

2. **Performance aceptable**
   - Dashboard carga en < 2 segundos
   - Vistas internas en < 1 segundo
   - Búsquedas instantáneas (< 500ms)

3. **Responsive funciona bien**
   - Valmore puede usar desde tablet en obra
   - Supervisor puede registrar avance desde móvil
   - Todas las funciones accesibles

4. **Multi-tenant está listo**
   - Aislamiento de datos funciona
   - Agregar empresa nueva toma < 5 minutos
   - Preparado para cliente #2

### Criterios de Negocio

**MVP será exitoso si:**

1. **Valmore está satisfecho**
   - Confirma que ahorra tiempo vs Excel
   - Tiene mejor visibilidad de sus proyectos
   - Recomienda el sistema a otro contratista

2. **Sistema es vendible**
   - Demo funciona perfectamente
   - Documentación de usuario completa
   - Puede ser replicado para cliente nuevo rápidamente

3. **SmartSolutions VE puede operar**
   - Deployment es manejable (no requiere DevOps dedicado)
   - Costos de servidor son sostenibles (< $50/mes)
   - Simón puede dar soporte sin ayuda externa

---

## 📚 REFERENCIAS Y RECURSOS

### Documentos relacionados

1. **Cuestionario de 50 preguntas** (ya preparado)
   - Para entrevista con Valmore
   - Ubicación: [ruta del archivo]

2. **Diseños de interfaz** (ya creados)
   - Dashboard principal
   - Nueva cotización
   - Proyecto en ejecución
   - Reporte financiero

3. **Guía de homologación SENIAT** (para futuro)
   - PA SNAT/2024/000121
   - Requisitos técnicos de facturación

### Stack técnico - Recursos

**Django:**
- Documentación oficial: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/

**Frontend:**
- HTMX: https://htmx.org/docs/
- Alpine.js: https://alpinejs.dev/
- Tailwind CSS: https://tailwindcss.com/docs

**Generación de documentos:**
- ReportLab (PDF): https://www.reportlab.com/documentation/
- OpenPyXL (Excel): https://openpyxl.readthedocs.io/

**Deployment:**
- DigitalOcean: https://docs.digitalocean.com/products/app-platform/

---

## 🎯 PRÓXIMOS PASOS

### Fase 0: Levantamiento de Información (AHORA)

1. **Entrevistar a Valmore**
   - Usar cuestionario de 50 preguntas
   - Documentar respuestas
   - Aclarar información CRÍTICA

2. **Recopilar activos**
   - Logo de la empresa
   - Excel con costos actuales (si existe)
   - Ejemplos de cotizaciones actuales

3. **Definir prioridades con Valmore**
   - ¿Qué módulo es más urgente?
   - ¿Qué puede esperar a versión 1.1?

### Fase 1: Setup y Fundamentos (Semana 1)

4. **Configurar proyecto Django**
   - Estructura de apps
   - PostgreSQL local
   - Git repository

5. **Implementar core multi-tenant**
   - Modelo Empresa
   - Modelo User extendido
   - Middleware de tenant
   - Autenticación

### Fase 2: Desarrollo Iterativo (Semanas 2-8)

6. **Seguir roadmap de desarrollo**
   - BD Costos (Semana 2)
   - Cotizaciones (Semanas 3-4)
   - Proyectos (Semanas 5-7)
   - Reportes (Semana 8)

7. **Testing continuo con Valmore**
   - Demo cada 2 semanas
   - Ajustar según feedback
   - Validar flujos de trabajo

### Fase 3: Pulido y Lanzamiento (Semana 9)

8. **Refinamiento final**
   - Responsive
   - Performance
   - Documentación

9. **Deployment a producción**
   - Configurar servidor
   - Migrar datos iniciales
   - Capacitar a Valmore

10. **Go Live**
    - Valmore empieza a usar 100%
    - Soporte cercano primeras semanas
    - Recoger feedback para v1.1

---

## 📝 NOTAS FINALES PARA CLAUDE CODE

**Este documento es tu contexto completo.** Úsalo como referencia durante todo el desarrollo del MVP.

**Cuando vayas a implementar:**
- Revisa la sección correspondiente en detalle
- Respeta la arquitectura multi-tenant definida
- Sigue los patrones de diseño especificados
- Implementa las validaciones de negocio descritas
- No olvides la matriz de permisos

**Cuando tengas dudas:**
- Consulta la sección "Información Faltante"
- Pregunta directamente a Simón
- No asumas: confirma antes de implementar

**Cuando completes un módulo:**
- Verifica que cumple criterios de éxito
- Prueba con datos de ejemplo
- Documenta cualquier decisión de implementación tomada

**Prioridad en todo momento:**
1. Funcionalidad correcta
2. Seguridad multi-tenant
3. Experiencia de usuario
4. Performance

---

**Versión del documento:** 1.0
**Fecha:** 19 de febrero de 2026
**Autor:** Simón Briceño - SmartSolutions VE
**Cliente:** Valmore
**Estado:** Listo para iniciar desarrollo - Pendiente completar información del cliente

---

_Este prompt será actualizado conforme se complete la información faltante y se tomen decisiones de implementación._