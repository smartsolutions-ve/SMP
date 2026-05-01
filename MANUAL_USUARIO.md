# Manual de Usuario — Smart Project Management v1.0

## Sistema para Industrias Técnicas Barquisimeto, C.A. (I.T.B.C.A.)

> Versión MVP 1.0 | Marzo 2026 | Desarrollado por SmartSolutions VE

---

## Tabla de Contenidos

1. [Inicio Rápido](#inicio-rápido)
2. [Flujo de Trabajo](#flujo-de-trabajo)
3. [Dashboard](#módulo-1-dashboard)
4. [Cotizaciones](#módulo-2-cotizaciones)
5. [Proyectos](#módulo-3-proyectos)
6. [Base de Datos de Costos](#módulo-4-base-de-datos-de-costos)
7. [Activos del Cliente](#módulo-5-activos-del-cliente)
8. [Nómina y Horas Hombre](#módulo-6-nómina-y-horas-hombre-hh)
9. [Reportes y Análisis](#módulo-7-reportes-y-análisis)
10. [Tema Claro / Oscuro](#tema-claro--oscuro)
11. [Roles y Permisos](#roles-y-permisos)
12. [Preguntas Frecuentes](#preguntas-frecuentes)
13. [Datos de Prueba](#datos-de-prueba-cargados)

---

## Inicio Rápido

**URL de acceso:** `http://127.0.0.1:8080/auth/login/`

**Usuarios del sistema:**

| Usuario   | Contraseña  | Rol                            |
|-----------|-------------|--------------------------------|
| `valmore` | `itbca2026` | Administrador (acceso completo)|
| `admin`   | `admin123`  | Super admin técnico (Django)   |

**Para arrancar el servidor** (desde terminal):

```bash
cd "/home/sabh/Documentos/Smart/Smart Project Management/smart_pm"
USE_SQLITE=true DJANGO_SETTINGS_MODULE=config.settings.development ../env/bin/python manage.py runserver 8080
```

**Navegación principal:** El sistema cuenta con un menú lateral (sidebar) permanente organizado en secciones:

| Sección        | Módulos                                      |
|----------------|----------------------------------------------|
| Principal      | Dashboard                                    |
| Gestión        | Cotizaciones, Proyectos, BD de Costos, Activos, Nómina HH |
| Análisis       | Reportes                                     |
| Configuración  | Admin (solo rol Administrador)               |

> **Nota sobre Formatos Numéricos:** Todo el sistema y los documentos generados utilizan el formato estándar local `es-VE`. Esto significa que debes emplear el **punto (.)** para delimitar los miles y la **coma (,)** para los decimales (Ejemplo: `1.234,56`).

---

## Flujo de Trabajo

El sistema sigue un flujo operativo lineal que refleja el ciclo de vida de un trabajo:

```
Registrar Equipo/Activo (opcional)
        ↓
Crear Cotización → Enviar → Aprobar → Convertir a Proyecto
                                              ↓
                                  Registrar Avance diario
                                  Registrar Horas Hombre
                                  Subir Fotos de evidencia
                                  Crear Órdenes de Cambio
                                              ↓
                                      Ver Reportes
```

**Resumen del flujo paso a paso:**

1. **(Opcional)** Registrar el equipo del cliente en **Activos** para trazabilidad
2. Crear una **Cotización** con las partidas de trabajo
3. Cambiar el estado de la cotización a **Enviada** cuando se envíe al cliente
4. Si el cliente acepta, marcar como **Aprobada**
5. **Convertir a Proyecto** indicando fechas de inicio y fin
6. Durante la ejecución, registrar **avance** diario por partida
7. Registrar las **horas hombre** consumidas por cargo
8. Subir **fotos** de evidencia del progreso
9. Consultar los **reportes** financieros para analizar rentabilidad

---

## Módulo 1: Dashboard

**Acceso:** Menú lateral → Dashboard / URL `/dashboard/`

![Dashboard principal del sistema](Manual%20de%20usuario/1.png)

El Dashboard es la pantalla principal al iniciar sesión. Muestra un resumen ejecutivo de la operación:

### Tarjetas de KPIs (parte superior)

| Indicador                  | Descripción                                           |
|---------------------------|-------------------------------------------------------|
| **Proyectos en curso**     | Cantidad de proyectos en estado "En Ejecución"       |
| **Cotizaciones sin respuesta** | Cotizaciones enviadas pendientes de respuesta del cliente |
| **Valor en ejecución**     | Suma total de contratos activos en USD               |
| **BD Costos**              | Acceso directo a gestión de precios                  |

### Alertas automáticas

El sistema muestra alertas cuando detecta situaciones que requieren atención:

- **Proyecto atrasado** (fondo azul): Cuando la fecha de fin planeada ya pasó y el proyecto sigue activo
- **Sobrecosto** (fondo amarillo): Cuando el costo real del proyecto supera el valor del contrato

### Secciones inferiores

- **Proyectos en Ejecución:** Lista de proyectos activos con su código, ubicación, estado, barra de avance y fechas
- **Cotizaciones:** Lista de las cotizaciones más recientes con estado y monto total

> El dashboard es de solo lectura. Para realizar acciones, navega al módulo correspondiente.

---

## Módulo 2: Cotizaciones

**Acceso:** Menú lateral → Cotizaciones / URL `/cotizaciones/`

![Lista de cotizaciones con filtros y estados](Manual%20de%20usuario/2.png)

### 2.1 Ver Lista de Cotizaciones

La pantalla principal muestra todas las cotizaciones de la empresa en una tabla con:

- **N° Cotización:** Código único asignado automáticamente (formato: COT-YYYY-XXX)
- **Cliente / Proyecto:** Nombre del cliente y del proyecto
- **Fecha:** Fecha de creación
- **Válida hasta:** Fecha de vencimiento de la oferta
- **Total:** Monto total en USD
- **Estado:** Badge de color según el estado actual
- **Acciones:** Botones de ver, editar, generar PDF y duplicar

**Filtros disponibles:**

| Filtro   | Descripción                                              |
|----------|----------------------------------------------------------|
| Buscar   | Por número de cotización, nombre de cliente o proyecto   |
| Estado   | Borrador, Enviada, Aprobada, Rechazada, Convertida       |
| Desde/Hasta | Rango de fechas de creación                           |

**Estados y sus significados:**

| Estado       | Color    | Significado                                        |
|-------------|----------|----------------------------------------------------|
| BORRADOR    | Gris     | Recién creada, aún no enviada al cliente           |
| ENVIADA     | Azul     | Enviada al cliente, esperando respuesta             |
| APROBADA    | Verde    | El cliente aprobó la propuesta                     |
| RECHAZADA   | Rojo     | El cliente rechazó la propuesta                    |
| VENCIDA     | Amarillo | Pasó la fecha de validez sin respuesta             |
| CONVERTIDA  | Púrpura  | Se convirtió exitosamente en un proyecto           |

---

### 2.2 Crear una Cotización Nueva

1. Ir a **Cotizaciones** en el menú lateral
2. Clic en el botón azul **"+ Nueva Cotización"**
3. Completar el formulario por secciones:

**Sección: Datos del Cliente**

| Campo                | Obligatorio | Descripción                                  |
|----------------------|:-----------:|----------------------------------------------|
| Nombre / Razón social | Si         | Nombre completo del cliente (ej: "Produsal, C.A.") |
| RIF                  | No          | Formato J-XXXXXXXX-X                        |
| Teléfono             | No          | Teléfono de contacto                         |
| Email                | No          | Correo electrónico                           |
| Persona de contacto  | No          | Nombre de la persona a tratar                |

**Sección: Datos del Proyecto**

| Campo                | Obligatorio | Descripción                                  |
|----------------------|:-----------:|----------------------------------------------|
| Nombre del proyecto  | Si          | Título descriptivo (ej: "Fabricación Canoa Autolimpiante") |
| Ubicación            | No          | Donde se realizará el trabajo                |
| Equipo/Activo asociado | No       | Seleccionar equipo del módulo Activos (si aplica) |
| Válida hasta         | Si          | Fecha de vencimiento (default: 15 días desde hoy) |
| Descripción del alcance | Si       | Detalle completo del trabajo a realizar      |

**Sección: Partidas** (tabla de ítems de trabajo)

Para agregar partidas hay dos opciones:

**Opción A — Agregar manualmente:**
1. Clic en el botón **"+ Agregar"**
2. Completar los campos de la fila que aparece:
   - **Código:** Opcional (ej: "01.01", "02.03")
   - **Descripción:** Nombre del ítem (obligatorio)
   - **Unidad:** Unidad de medida (un, ml, kg, dia, hora, etc.)
   - **Sección:** Categoría del trabajo (ej: "SERVICIOS MECÁNICOS")
   - **Cant.:** Cantidad numérica
   - **P.Unit.:** Precio unitario en USD
   - El **Subtotal** se calcula automáticamente (Cantidad x P.Unit.)

**Opcion B — Buscar en Base de Datos de Costos:**
1. Clic en el botón **"Buscar en BD Costos"**
2. Escribir al menos 2 letras en el campo de búsqueda (ej: "bomba", "sold")
3. Clic en el resultado deseado
4. El ítem se agrega automáticamente con su código, descripción, unidad y precio actual

**Sección lateral: Totales y Configuración**

| Campo                  | Descripción                                           |
|-----------------------|-------------------------------------------------------|
| Margen de utilidad (%) | Porcentaje de ganancia sobre el subtotal (default: 15%) |
| Subtotal              | Suma de todas las partidas (se calcula automáticamente) |
| Utilidad              | Subtotal x Margen % (se calcula automáticamente)       |
| **TOTAL**             | Subtotal + Utilidad (se calcula automáticamente)       |
| Términos y condiciones | Se carga automáticamente con los estándares de I.T.B.C.A. Puedes editarlos |
| Notas internas        | Solo visibles para el equipo, no aparecen en el PDF    |

**Para guardar:**
- Clic en el botón verde **"Crear cotización"**
- El sistema asigna automáticamente un número (COT-YYYY-XXX)
- Serás redirigido al detalle de la cotización

> **IMPORTANTE:** Debes tener al menos **UNA partida** para poder guardar. Si el botón "Crear cotización" no hace nada, asegúrate de haber agregado partidas.

---

### 2.3 Ver Detalle de una Cotización

Clic en el icono de **ojo** en cualquier cotización de la lista. El detalle muestra:

- Información completa del cliente y del proyecto
- Equipo/activo asociado (si existe)
- Tabla de partidas con código, descripción, unidad, cantidad, precio y subtotal
- Totales: subtotal, utilidad, total
- Términos y condiciones
- Botones de acción según el estado actual

---

### 2.4 Cambiar el Estado de una Cotización

En la pantalla de detalle, los botones disponibles dependen del estado actual:

| Estado actual | Acciones disponibles                              |
|--------------|---------------------------------------------------|
| BORRADOR     | Marcar como Enviada, Editar, Duplicar, PDF        |
| ENVIADA      | Aprobar, Rechazar, Editar, Duplicar, PDF          |
| APROBADA     | Convertir a Proyecto, Duplicar, PDF               |
| RECHAZADA    | Duplicar, PDF                                     |
| CONVERTIDA   | Ver proyecto asociado, PDF                        |

---

### 2.5 Editar una Cotización

Solo se pueden editar cotizaciones en estado **BORRADOR** o **ENVIADA**.

1. En el detalle de la cotización, clic en el icono de **lápiz** (Editar)
2. El formulario se carga con todos los datos actuales incluyendo las partidas
3. Modifica lo necesario y clic en **"Guardar cambios"**

> Si la cotización está en APROBADA, RECHAZADA o CONVERTIDA, no se puede editar. Usa **Duplicar** para crear una copia editable.

---

### 2.6 Duplicar una Cotización

En el detalle, clic en el icono de **copiar** (Duplicar). Crea una copia exacta en estado BORRADOR con todas las partidas, listo para ajustar y reutilizar.

---

### 2.7 Generar PDF

En el detalle, clic en el icono **rojo de PDF**. Se genera un documento PDF profesional con:

- Encabezado con datos de la empresa (I.T.B.C.A.)
- Número de cotización, fecha y estado
- Datos del cliente y del proyecto
- Tabla de partidas con subtotales
- Totales (subtotal, utilidad, total en USD)
- Términos y condiciones
- Pie de página con datos fiscales

El PDF se abre en una nueva pestaña del navegador y puede descargarse o imprimirse.

> **Nota de espera:** La generación del documento es un proceso pesado; verás un indicador de carga giratorio en el botón mientras se genera. Por favor, espera y evita hacer múltiples clics.

> **Nota:** El margen de utilidad se muestra como "Utilidad" en el PDF sin indicar el porcentaje, para no revelar el margen al cliente.

---

## Módulo 3: Proyectos

**Acceso:** Menú lateral → Proyectos / URL `/proyectos/`

![Lista de proyectos con tarjetas de estado y avance](Manual%20de%20usuario/3.png)

### 3.1 Ver Lista de Proyectos

La pantalla muestra tarjetas individuales por cada proyecto con:

- **Código:** PROY-YYYY-XXX (asignado automáticamente)
- **Estado:** Badge de color (En Ejecución, Atrasado, Planificación, etc.)
- **Nombre y ubicación del proyecto**
- **Barra de avance físico** con porcentaje
- **Datos financieros:** Valor contrato, costo real, utilidad
- **Fechas:** Inicio → Fin planeado (en rojo si está atrasado)
- **Gerente:** Usuario responsable del proyecto

**Filtro por estado:** Clic en los badges superiores para filtrar (Todos, Planificación, En Ejecución, Pausado, Completado, Cancelado).

---

### 3.2 Convertir Cotización en Proyecto

**Requisito:** La cotización debe estar en estado **APROBADA**.

1. Ir al detalle de la cotización aprobada
2. Clic en el botón **"Convertir a Proyecto"**
3. En el modal que aparece, completar:
   - **Fecha de inicio:** Cuándo empieza el trabajo
   - **Fecha de fin planeada:** Cuándo se planea terminar
4. Clic en **"Crear Proyecto"**

El sistema crea automáticamente:
- Un proyecto con código PROY-YYYY-XXX
- Todas las partidas de la cotización copiadas como partidas del proyecto
- El equipo/activo asociado (si la cotización tenía uno)
- La cotización pasa a estado **CONVERTIDA**

---

### 3.3 Ver Detalle de un Proyecto

Clic en cualquier tarjeta de proyecto. El detalle tiene **4 pestañas:**

**Pestaña 1: Resumen**
- Información general del proyecto y del cliente
- KPIs principales: valor contrato, costo real, utilidad, avance %
- Equipo/activo asociado (si existe)
- Botones para cambiar el estado del proyecto

**Pestaña 2: Partidas**
- Tabla con todas las partidas mostrando:
  - Código y descripción
  - Cantidad presupuestada vs cantidad ejecutada
  - Costo presupuestado vs costo real
  - Variación en costo (rojo si hay sobrecosto)
  - Barra de avance individual con porcentaje
  - Estado (Sin iniciar, En proceso, Completa)
- Botones por partida:
  - **"+ Avance"**: Registrar avance del día
  - **Reloj**: Registrar horas hombre (HH)

**Pestaña 3: Avance / Fotos**
- Galería de las últimas 12 fotos del proyecto
- Formulario para subir nuevas fotos (máx. 10 por carga, 5MB por foto)

**Pestaña 4: Órdenes de Cambio**
- Lista de cambios al alcance original con su impacto en costo y tiempo
- Botón para crear nueva orden de cambio

---

### 3.4 Cambiar Estado del Proyecto

En la pestaña Resumen, hay botones según el estado actual:

| Estado actual     | Botones disponibles                          |
|-------------------|----------------------------------------------|
| PLANIFICACION     | Iniciar Ejecución                            |
| EN_EJECUCION      | Pausar, Completar                            |
| PAUSADO           | Reanudar Ejecución                           |
| EN_EJECUCION/PAUSADO | Cancelar                                  |

**Comportamientos automáticos:**
- Al hacer clic en botones de estado definitivo (Ej: Completar proyecto) aparecerá una **ventana modal de confirmación** para protegerte de clics accidentales.
- Al pasar a **EN_EJECUCION** → Se registra automáticamente la **fecha de inicio real**
- Al pasar a **COMPLETADO** → Se registra automáticamente la **fecha de fin real**

---

### 3.5 Registrar Avance de una Partida

**Requisito:** El proyecto debe estar en estado **EN_EJECUCION** o **PAUSADO**.

1. Ir al detalle del proyecto → Pestaña **Partidas**
2. Clic en **"+ Avance"** en la partida correspondiente
3. Completar el formulario:

| Campo              | Obligatorio | Descripción                                |
|--------------------|:-----------:|--------------------------------------------|
| Fecha              | Si          | Fecha del trabajo (no puede ser futura)    |
| Cantidad ejecutada | Si          | Cuánto se hizo ese día/jornada             |
| Costo del día      | Si          | Cuánto costó en USD (0 = solo avance físico)|
| Observaciones      | No          | Notas del trabajo realizado                |

4. Clic en **"Guardar Registro"**

> **Nota de Confirmación:** Un modal interactivo te pedirá que re-confirmes la acción antes de guardarse permanentemente.

> **IMPORTANTE:** Los registros de avance son **INMUTABLES**. Una vez guardado, no se puede editar ni eliminar. Si cometiste un error, crea un nuevo registro con valores de corrección (ej: cantidad negativa).

**Cálculos automáticos tras registrar:**
- Se actualiza la **cantidad ejecutada** acumulada de la partida
- Se recalcula el **% de avance** de la partida (ejecutado / presupuestado)
- Se recalcula el **avance general** del proyecto (promedio ponderado por costo)
- Si la partida llega al 100%, pasa automáticamente a estado **Completada**

---

### 3.6 Subir Fotos del Proyecto

1. Ir al detalle del proyecto → Pestaña **Avance / Fotos**
2. En el formulario inferior:
   - Escribir una descripción de las fotos
   - Clic en **"Seleccionar fotos"** y elegir imágenes
   - Máximo 10 fotos por carga, 5MB por foto
3. Clic en **"Subir Fotos"**

---

### 3.7 Crear Orden de Cambio

Cuando el cliente solicita cambios al alcance original del proyecto:

1. En el detalle del proyecto → Pestaña **Órdenes de Cambio**
2. Clic en **"+ Nueva Orden de Cambio"**
3. Completar:

| Campo               | Descripción                                          |
|---------------------|------------------------------------------------------|
| Descripción         | Qué cambió en el alcance                             |
| Justificación       | Por qué se necesita el cambio                        |
| Impacto en costo ($)| Cuánto sube o baja el valor (positivo o negativo)    |
| Impacto en tiempo   | Cuántos días se extiende o reduce el plazo           |

4. Clic en **"Crear OC"**

La orden queda en estado **PENDIENTE**. Un usuario con rol Admin o Gerente puede **Aprobar** o **Rechazar** la orden.

**Al aprobar una orden de cambio:**
- El valor del contrato se ajusta automáticamente según el impacto en costo
- La fecha de fin planeada se extiende según el impacto en tiempo

---

## Módulo 4: Base de Datos de Costos

**Acceso:** Menú lateral → BD de Costos / URL `/bd-costos/`

![Base de Datos de Costos con ítems y filtros](Manual%20de%20usuario/4.png)

Repositorio centralizado de precios actualizados de materiales, mano de obra, equipos y subcontratos. Los ítems de esta base se utilizan como referencia al crear cotizaciones.

### 4.1 Ver Ítems de Costo

La tabla muestra todos los ítems registrados con:
- **Código:** Identificador único (ej: MO-SOL, MAT-ROD)
- **Descripción:** Nombre completo del ítem
- **Tipo:** Material, Mano de Obra, Equipo/Maquinaria, Subcontrato, Otros
- **Categoría:** Clasificación jerárquica (hasta 3 niveles)
- **Unidad:** m², kg, ml, un, dia, hora, etc.
- **Precio:** Precio actual en la moneda indicada
- **Moneda:** USD o VES
- **Últ. Act.:** Fecha de la última actualización de precio
- **Estado:** Activo o Inactivo

**Filtros disponibles:**

| Filtro    | Opciones                                    |
|-----------|---------------------------------------------|
| Buscar    | Por código o descripción                    |
| Tipo      | Material, Mano de Obra, Equipo, etc.       |
| Categoría | Cualquier categoría registrada              |
| Estado    | Activos, Inactivos, Todos                   |

---

### 4.2 Crear un Nuevo Ítem

1. Clic en **"+ Nuevo Ítem"**
2. Completar:

| Campo                 | Obligatorio | Descripción                              |
|-----------------------|:-----------:|------------------------------------------|
| Código                | Si          | Identificador único (ej: "MAT-003")     |
| Tipo                  | Si          | Material / Mano de Obra / Equipo / etc. |
| Descripción           | Si          | Nombre completo del ítem                 |
| Unidad                | Si          | Unidad de medida                         |
| Categoría             | No          | Seleccionar de la lista o dejar vacío    |
| Precio actual         | Si          | Precio unitario en USD                   |
| Moneda                | Si          | USD o VES                                |
| Especificaciones      | No          | Normas, características técnicas, marca  |
| Proveedor preferido   | No          | Nombre del proveedor                     |
| Notas internas        | No          | Observaciones para uso interno           |

3. Clic en **"Crear ítem"**

---

### 4.3 Editar un Ítem y Actualizar Precio

1. Clic en el icono de **lápiz** del ítem
2. Modificar los campos necesarios
3. Si cambias el precio, opcionalmente indicar la razón del cambio
4. Clic en **"Guardar cambios"**

El historial de precios se registra automáticamente cada vez que el precio cambia.

---

### 4.4 Ver Historial de Precios

1. Clic en el icono de **gráfica** del ítem
2. Se muestra:
   - Gráfica de evolución del precio en el tiempo
   - Tabla con cada cambio: fecha, precio anterior, precio nuevo, observación

---

### 4.5 Categorías

**Acceso:** BD Costos → botón **"Categorías"**

Permite crear y organizar las categorías de ítems en hasta **3 niveles** jerárquicos. Ejemplo:

```
01 FABRICACIÓN
  ├── 01.01 Materiales de Fabricación
  └── 01.02 Consumibles de Soldadura
02 MANO DE OBRA
  ├── 02.01 Técnicos Especializados
  └── 02.02 Ayudantes
```

Para crear una categoría:
1. Ingresar nombre, código y (opcionalmente) categoría padre
2. Clic en **"Crear"**

---

## Módulo 5: Activos del Cliente

**Acceso:** Menú lateral → Activos / URL `/activos/`

![Registro de activos/equipos del cliente](Manual%20de%20usuario/5.png)

Este módulo permite registrar los equipos, maquinaria e infraestructura de los clientes. Cada activo puede asociarse a cotizaciones y proyectos para mantener la trazabilidad completa del historial de trabajos realizados sobre un equipo.

### 5.1 Ver Lista de Activos

La pantalla principal muestra todos los equipos registrados con:

- **Código/TAG:** Identificador único del equipo (ej: BOM-AC-001)
- **Nombre:** Descripción del equipo
- **Tipo:** Bomba, Calderín, Tanque, Tubería, Intercambiador, etc.
- **Cliente:** Propietario del equipo
- **Ubicación:** Planta o instalación donde se encuentra
- **Marca / Modelo:** Fabricante y modelo
- **Estado:** Operativo, En Reparación, Fuera de Servicio, Retirado
- **Mtto.:** Días para el próximo mantenimiento o indicador de mantenimiento vencido

**Indicadores de estado:**

| Estado         | Color    | Significado                                |
|---------------|----------|--------------------------------------------|
| OPERATIVO     | Verde    | Equipo funcionando normalmente             |
| EN_REPARACION | Amarillo | Equipo en proceso de reparación            |
| FUERA_SERVICIO| Rojo     | Equipo fuera de operación                  |
| RETIRADO      | Gris     | Equipo dado de baja                        |

**Alerta de mantenimiento:** Los equipos con mantenimiento vencido muestran un badge amarillo **"Vencido"** para identificar rápidamente qué equipos requieren atención.

**Filtros disponibles:**

| Filtro  | Opciones                                          |
|---------|---------------------------------------------------|
| Buscar  | Por código, nombre, marca o serial                |
| Tipo    | Bomba, Calderín, Tanque, etc.                    |
| Estado  | Operativo, En Reparación, Fuera de Servicio, etc.|
| Cliente | Lista de clientes propietarios                    |

---

### 5.2 Registrar un Nuevo Equipo

1. Clic en **"+ Registrar Equipo"**
2. Completar el formulario por secciones:

**Identificación del Equipo:**

| Campo        | Obligatorio | Descripción                                      |
|-------------|:-----------:|--------------------------------------------------|
| Código/TAG  | Si          | Identificador único del equipo (ej: BOM-AC-001) |
| Tipo        | Si          | Seleccionar de la lista (Bomba, Tanque, etc.)    |
| Nombre      | Si          | Descripción completa del equipo                  |
| Marca       | No          | Fabricante (ej: Grundfos, Alfa Laval)           |
| Modelo      | No          | Modelo del equipo (ej: CR 32-2)                 |
| Serial      | No          | Número de serie                                  |

**Cliente y Ubicación:**

| Campo              | Obligatorio | Descripción                              |
|-------------------|:-----------:|------------------------------------------|
| Cliente propietario| Si          | Nombre del cliente dueño del equipo      |
| RIF del cliente   | No          | RIF del cliente propietario              |
| Ubicación/Planta  | No          | Instalación donde se encuentra           |
| Área/Sección      | No          | Área específica dentro de la planta      |

**Estado y Mantenimiento:**

| Campo                  | Obligatorio | Descripción                                    |
|-----------------------|:-----------:|------------------------------------------------|
| Estado                | Si          | Operativo, En Reparación, Fuera de Servicio, Retirado |
| Fecha de instalación  | No          | Cuándo se instaló el equipo                    |
| Frecuencia de mtto.   | No          | Cada cuántos días requiere mantenimiento preventivo |
| Próximo mantenimiento | No          | Fecha del próximo mantenimiento programado     |

**Detalles Adicionales:**

| Campo                  | Obligatorio | Descripción                              |
|-----------------------|:-----------:|------------------------------------------|
| Especificaciones técnicas | No      | Capacidad, presión, temperatura, materiales, etc. |
| Notas                 | No          | Observaciones adicionales                |

3. Clic en **"Registrar equipo"**

---

### 5.3 Ver Detalle de un Activo

Clic en el icono de **ojo** del equipo. El detalle muestra:

- **Tarjetas de resumen:** Estado actual, próximo mantenimiento, frecuencia
- **Datos del equipo:** Tipo, marca, modelo, serial, fecha de instalación
- **Ubicación y cliente:** Propietario, RIF, ubicación, área
- **Especificaciones técnicas:** Detalle completo del equipo
- **Cotizaciones asociadas:** Todas las cotizaciones que mencionan este equipo
- **Proyectos asociados:** Todos los proyectos vinculados a este equipo

Esta vista permite ver el **historial completo de trabajos** realizados sobre un equipo a lo largo del tiempo.

---

### 5.4 Asociar un Activo a una Cotización

Al crear o editar una cotización, en la sección "Datos del Proyecto" existe el campo **"Equipo/Activo asociado"**. Al seleccionar un activo:

- La cotización queda vinculada al equipo
- Si la cotización se convierte en proyecto, el vínculo se copia automáticamente
- En el detalle del activo se puede ver el historial de cotizaciones y proyectos

---

### 5.5 API de Búsqueda de Activos

El sistema ofrece un endpoint de búsqueda rápida: `/activos/api/buscar/?q=bomba`

Retorna resultados en formato JSON con código, nombre, tipo, cliente, ubicación y estado. Útil para integraciones futuras o formularios dinámicos.

---

## Módulo 6: Nómina y Horas Hombre (HH)

**Acceso:** Menú lateral → Nómina HH / URL `/nomina/`

> **Nota:** Este módulo solo es visible para usuarios con permiso de ver costos (roles Admin y Gerente). Los Supervisores no tienen acceso.

![Lista de cargos y tarifas por hora](Manual%20de%20usuario/6.png)

Este módulo permite gestionar los cargos de trabajadores con sus tarifas por hora, y registrar las horas hombre consumidas en cada partida de un proyecto.

### 6.1 Ver Lista de Cargos

La tabla muestra todos los cargos registrados con:

- **Código:** Identificador único (ej: SOL-6G, TUB-01)
- **Nombre del Cargo:** Descripción del cargo (ej: Soldador certificado 6G)
- **Nivel:** Categoría del cargo
- **Costo/Hora:** Tarifa por hora en USD
- **Moneda:** USD o VES
- **BD Costos:** Indica si el cargo está vinculado a la BD de Costos
- **Estado:** Activo o Inactivo

**Niveles de cargo:**

| Nivel        | Descripción                                    | Rango típico USD/h |
|-------------|------------------------------------------------|---------------------|
| AYUDANTE    | Personal de apoyo sin especialización          | $5 - $8            |
| OFICIAL     | Técnico con experiencia estándar               | $10 - $15          |
| MAESTRO     | Técnico altamente experimentado                | $14 - $18          |
| ESPECIALISTA| Certificaciones específicas (ej: 6G)           | $16 - $22          |
| SUPERVISOR  | Encargado de obra con personal a cargo         | $20 - $25          |
| INGENIERO   | Profesional con título universitario           | $25 - $35          |

---

### 6.2 Crear un Nuevo Cargo

1. Clic en **"+ Nuevo Cargo"**
2. Completar:

| Campo        | Obligatorio | Descripción                                  |
|-------------|:-----------:|----------------------------------------------|
| Código      | Si          | Identificador único (ej: SOL-6G)            |
| Nivel       | Si          | Seleccionar de la lista                      |
| Nombre      | Si          | Nombre descriptivo del cargo                 |
| Descripción | No          | Funciones, certificaciones requeridas        |
| Costo/hora  | Si          | Tarifa por hora en USD                       |
| Moneda      | Si          | USD o VES                                    |

**Sincronización con BD de Costos:**

Activar la casilla **"Sincronizar con BD de Costos"** para crear automáticamente un ítem de tipo **MANO DE OBRA** en la BD de Costos con el código `HH-{código}` y la tarifa del cargo. Esto permite usar el cargo directamente en cotizaciones desde la BD de Costos.

3. Clic en **"Crear cargo"**

---

### 6.3 Ver Detalle de un Cargo

Clic en el icono de **ojo** del cargo. El detalle muestra:

- **Métricas:** Costo/hora actual, total horas registradas, costo total acumulado, cantidad de registros
- **Vinculación BD Costos:** Si está sincronizado, muestra el ítem vinculado
- **Historial de tarifas:** Tabla con cada cambio de tarifa (fecha, tarifa anterior, tarifa nueva, variación, razón del cambio)

---

### 6.4 Actualizar Tarifa de un Cargo

1. Clic en el icono de **lápiz** del cargo
2. Modificar el campo **"Costo por hora"**
3. Indicar la razón del cambio (ej: "Ajuste anual", "Nuevo convenio colectivo")
4. Si está activada la sincronización, el ítem en BD de Costos se actualiza automáticamente
5. Clic en **"Guardar cambios"**

El cambio queda registrado en el historial de tarifas con fecha, usuario y razón.

---

### 6.5 Registrar Horas Hombre en un Proyecto

**Acceso:** Desde el detalle de un proyecto → Pestaña Partidas → Botón del **reloj** en la partida

Esta es la función principal del módulo. Permite registrar cuántas horas trabajó cada tipo de cargo en una partida específica del proyecto.

**Formulario de registro:**

| Campo               | Obligatorio | Descripción                                    |
|--------------------|:-----------:|------------------------------------------------|
| Cargo              | Si          | Seleccionar de la lista (muestra tarifa/hora)  |
| Fecha              | Si          | Fecha del trabajo (no puede ser futura)        |
| Trabajadores       | Si          | Cantidad de personas de ese cargo (default: 1) |
| Horas              | Si          | Horas trabajadas (paso de 0.25 = 15 minutos)  |
| Observaciones      | No          | Actividad realizada                            |

**Cálculo del costo:**

```
Costo total = Cantidad de trabajadores x Horas x Costo/hora del cargo
```

Ejemplo: 2 soldadores 6G x 8 horas x $18.00/h = **$288.00**

> **IMPORTANTE:** El costo por hora se toma como **snapshot** al momento del registro. Si la tarifa del cargo cambia después, los registros anteriores mantienen la tarifa con la que fueron creados.

**Registros existentes:** En la parte derecha se muestra la tabla de todos los registros de HH de esa partida con:
- Fecha, cargo, cantidad de trabajadores, horas, costo/hora aplicado, costo total
- Total acumulado de costo HH en la partida

Los registros de HH son **inmutables** (no se pueden editar ni eliminar).

---

## Módulo 7: Reportes y Análisis

**Acceso:** Menú lateral → Reportes / URL `/reportes/`

> **Nota:** Solo accesible para usuarios con permiso de ver costos (roles Admin y Gerente).

![Reportes financieros con gráficas y KPIs](Manual%20de%20usuario/7.png)

El módulo de reportes ofrece un análisis financiero completo de la operación con gráficas interactivas y tablas detalladas.

### 7.1 Rango de Fechas

En la parte superior se puede seleccionar el período de análisis:
- **Desde:** Fecha de inicio del período (default: hace 1 año)
- **Hasta:** Fecha de fin del período (default: hoy)
- Clic en **"Actualizar"** para aplicar el filtro

### 7.2 Tarjetas de Resumen

| Indicador       | Descripción                                              |
|-----------------|----------------------------------------------------------|
| Total Proyectos | Cantidad de proyectos en el período seleccionado         |
| Valor Total ($) | Suma de valores de contrato de todos los proyectos       |
| Utilidad Total  | Diferencia entre valor de contratos y costos reales      |
| Margen Promedio | Porcentaje promedio de utilidad sobre valor de contrato  |

### 7.3 Gráfica: Valor vs Costo Real por Proyecto

Gráfica de barras (Chart.js) que compara visualmente para cada proyecto:
- **Barra azul:** Valor del contrato
- **Barra roja:** Costo real acumulado
- **Barra verde:** Utilidad (contrato - costo)

Permite identificar rápidamente qué proyectos son rentables y cuáles tienen sobrecosto.

### 7.4 Análisis de Cotizaciones

Panel lateral con estadísticas de cotizaciones:
- Total de cotizaciones en el período
- Aprobadas/Convertidas vs Rechazadas vs Pendientes
- **Tasa de conversión:** % de cotizaciones que se convierten en proyecto
- **Valor aprobado:** Suma de montos de cotizaciones aprobadas
- **Gráfica de dona:** Distribución visual por estado

![Tabla de rentabilidad por proyecto](Manual%20de%20usuario/8.png)

### 7.5 Tabla: Rentabilidad por Proyecto

Tabla detallada con cada proyecto mostrando:

| Columna        | Descripción                                            |
|----------------|--------------------------------------------------------|
| Proyecto       | Código y nombre del proyecto                           |
| Cliente        | Nombre del cliente                                     |
| Estado         | Estado actual del proyecto                             |
| Valor Contrato | Monto del contrato en USD                              |
| Costo Real     | Gasto real acumulado                                   |
| Utilidad       | Contrato - Costo real (verde si positivo, rojo si negativo) |
| Margen %       | Porcentaje de utilidad sobre el valor del contrato     |

La fila **TOTALES** al final resume la operación completa.

---

## Tema Claro / Oscuro

En la parte inferior del menú lateral hay un toggle **Sol/Luna** para cambiar entre:

- **Modo claro:** Fondo blanco/gris claro, texto oscuro. Ideal para uso diurno o en ambientes bien iluminados
- **Modo oscuro:** Fondo oscuro con efecto glassmorphism, texto claro. Reduce fatiga visual en ambientes con poca luz

La preferencia se guarda en el navegador y se mantiene entre sesiones. No requiere iniciar sesión nuevamente.

---

## Roles y Permisos

El sistema maneja 4 roles con diferentes niveles de acceso:

| Acción                         | Admin | Gerente | Supervisor | Cliente |
|--------------------------------|:-----:|:-------:|:----------:|:-------:|
| Ver dashboard                  |  Si   |   Si    |    Si      |   No    |
| Crear/editar cotizaciones      |  Si   |   Si    |    No      |   No    |
| Aprobar/rechazar cotizaciones  |  Si   |   Si    |    No      |   No    |
| Generar PDF de cotización      |  Si   |   Si    |    No      |   No    |
| Convertir cotización a proyecto|  Si   |   Si    |    No      |   No    |
| Ver costos y precios           |  Si   |   Si    |    No      |   No    |
| Registrar avance en proyectos  |  Si   |   Si    |    Si*     |   No    |
| Subir fotos de evidencia       |  Si   |   Si    |    Si*     |   No    |
| Aprobar órdenes de cambio      |  Si   |   Si    |    No      |   No    |
| Gestionar BD de Costos         |  Si   |   Si    |    No      |   No    |
| Gestionar Activos              |  Si   |   Si    |    Si      |   No    |
| Ver/gestionar Nómina HH        |  Si   |   Si    |    No      |   No    |
| Registrar horas hombre         |  Si   |   Si    |    No      |   No    |
| Ver reportes financieros       |  Si   |   Si    |    No      |   No    |
| Acceder al Admin Django        |  Si   |   No    |    No      |   No    |

*El Supervisor solo puede acceder a los proyectos donde está asignado como supervisor.

---

## Preguntas Frecuentes

**P: No puedo crear una cotización, el botón no hace nada.**
R: Debes tener al menos **una partida** agregada antes de guardar. Clic en "+ Agregar" para añadir una fila de partida, completa los campos y luego intenta guardar.

**P: No puedo editar una cotización.**
R: Solo se pueden editar cotizaciones en estado **BORRADOR** o **ENVIADA**. Si la cotización está Aprobada, Rechazada o Convertida, usa el botón **"Duplicar"** para crear una copia editable.

**P: Cometí un error en un registro de avance, ¿cómo lo corrijo?**
R: Los registros de avance son **inmutables** por diseño (auditoría). Para corregir, crea un nuevo registro con los valores inversos. Ejemplo: si registraste 10 unidades por error, crea otro registro con -10 unidades.

**P: ¿Puedo crear un proyecto sin cotización?**
R: Actualmente no. El flujo es: Cotización → Aprobar → Convertir a Proyecto. Esto garantiza que todo proyecto tiene un respaldo comercial documentado.

**P: ¿Por qué el avance del proyecto no es el promedio simple de las partidas?**
R: El avance general usa **promedio ponderado** por costo presupuestado. Una partida de $10,000 tiene más peso en el avance total que una de $500, reflejando mejor la realidad del proyecto.

**P: ¿Qué pasa cuando el costo real supera el presupuestado?**
R: La partida llega al 100% de avance físico (no puede pasar de 100%), pero el costo real sigue sumando. La utilidad del proyecto se mostrará en rojo (negativa) en el dashboard y los reportes.

**P: ¿El PDF se envía automáticamente al cliente?**
R: No. El PDF se genera para ver/descargar. El envío al cliente se hace manualmente (email, WhatsApp, etc.).

**P: ¿Cómo vinculo un equipo a una cotización?**
R: Al crear o editar la cotización, en la sección "Datos del Proyecto" hay un campo selector "Equipo/Activo asociado". Si el equipo no existe, primero regístralo en el módulo Activos.

**P: Si cambio la tarifa de un cargo, ¿se actualizan los registros anteriores?**
R: No. Cada registro de HH guarda un **snapshot** de la tarifa al momento de crearse. Los registros anteriores mantienen la tarifa original. Solo los registros futuros usarán la nueva tarifa.

**P: ¿Qué significa "Sincronizar con BD de Costos" en Nómina?**
R: Crea automáticamente un ítem de tipo MANO DE OBRA en la BD de Costos con la tarifa del cargo. Así puedes usar el cargo como referencia al crear partidas en cotizaciones.

---

## Datos de Prueba Cargados

El sistema viene precargado con datos reales de I.T.B.C.A. para demostración:

### Cotizaciones

| Número         | Cliente           | Proyecto                           | Estado     | Total      |
|---------------|-------------------|------------------------------------|------------|------------|
| COT-2025-2836 | Plata Catia La Mar| Reparación Bomba Agua Caliente     | APROBADA   | $6,595.54  |
| COT-2026-2864 | Plata Catia La Mar| Toma Muestra Calderín 1 y 2        | CONVERTIDA | $754.74    |
| COT-2026-2865 | Produsal          | Canoa Autolimpiante Sin Fin #1     | BORRADOR   | $13,822.25 |
| COT-2026-003  | Produsal          | Canoa Autolimpiante (Copia)        | BORRADOR   | $13,822.25 |

### Proyectos

| Código        | Nombre                              | Estado       | Avance  |
|--------------|-------------------------------------|-------------|---------|
| PROY-2026-001| Reparación Bomba Agua Caliente      | En Ejecución| ~80%    |
| PROY-2026-002| Toma Muestra Calderín 1 y 2         | En Ejecución| ~50%    |

### Activos del Cliente

| Código/TAG  | Nombre                              | Cliente           | Estado        |
|------------|-------------------------------------|-------------------|---------------|
| BOM-AC-001 | Bomba centrífuga agua caliente      | Hotel Meliá Caracas| En Reparación|
| CAL-001    | Calderín vapor horizontal           | Produsal C.A.     | Operativo     |
| TQ-AI-001  | Tanque almacenamiento inoxidable    | Produsal C.A.     | Operativo     |
| IC-001     | Intercambiador de calor de placas   | Hotel Meliá Caracas| Operativo    |
| CAN-001    | Canoa autolimpiante para evaporador | Produsal C.A.     | Operativo     |

### Cargos de Nómina

| Código  | Nombre                    | Nivel        | Costo/Hora |
|---------|---------------------------|-------------|------------|
| SOL-6G  | Soldador certificado 6G   | Especialista| $18.00     |
| SOL-3G  | Soldador 3G               | Oficial     | $14.00     |
| TUB-01  | Tubero/Montador            | Oficial     | $12.00     |
| MEC-01  | Mecánico industrial        | Oficial     | $13.00     |
| AYU-01  | Ayudante de taller         | Ayudante    | $7.00      |
| SUP-01  | Supervisor de obra         | Supervisor  | $22.00     |
| ING-01  | Ingeniero de proyecto      | Ingeniero   | $28.00     |
| PUL-01  | Pulidor/Acabado            | Maestro     | $15.00     |
| CAL-01  | Calderero                  | Maestro     | $16.00     |
| PIN-01  | Pintor industrial          | Oficial     | $10.00     |

### BD de Costos
18 ítems organizados en 12 categorías con precios reales de I.T.B.C.A.

---

*Manual de Usuario v1.0 — Smart Project Management*
*SmartSolutions VE | Marzo 2026*
*Desarrollado por Simón Briceño y Javier Figueroa*
