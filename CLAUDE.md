# CLAUDE.md — Smart Project Management

Instrucciones para Claude Code al trabajar en este proyecto.

## Stack

| Capa | Tecnología | Notas |
|------|-----------|-------|
| Backend | Django 6.0.3 + Python 3.x | |
| Base de datos | PostgreSQL (producción), SQLite (desarrollo) | |
| Frontend | Django Templates + HTMX + Alpine.js + Tailwind | |
| Auth | AbstractUser (`Usuario`) | UUID PK |
| Deploy | PythonAnywhere | |
| Reportes | reportlab + openpyxl | |
| Imágenes | Pillow | |

## Estructura del proyecto

```
smart_pm/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/          → Empresa (tenant UUID), Usuario
│   ├── proyectos/     → Proyecto, Tarea, HitoProyecto
│   ├── cotizaciones/  → Cotizacion, ItemCotizacion
│   ├── activos/       → Activos físicos
│   ├── bd_costos/     → Base de datos de costos
│   ├── nomina/        → Gestión de nómina
│   └── reportes/      → Vistas de reportes
├── static/
├── media/
├── requirements/
│   └── base.txt
└── manage.py
```

## Multi-tenancy

**A diferencia de SmartSales**, este proyecto usa UUID en todos los modelos principales.

- El modelo tenant se llama `Empresa` (no `Organization`)
- El usuario se llama `Usuario` (no `User`)
- Ambos tienen `id = UUIDField(primary_key=True)`
- Los modelos hijo usan `empresa = ForeignKey(Empresa, ...)`
- **No hay TenantMiddleware** — el aislamiento se hace manualmente en cada vista

## Reglas de desarrollo

1. **Siempre filtrar por `empresa`** en cualquier queryset de modelos tenant-aware
2. **UUID en nuevos modelos**: `id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)`
3. Modelo tenant se llama `Empresa`, FK se llama `empresa` (no `organization`)
4. Sin Docker — deploy directo en PythonAnywhere

## Comandos de desarrollo

```bash
# Activar entorno virtual
source venv/bin/activate   # o el venv que uses

# Desarrollo
python manage.py runserver

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Tests
pytest
```

## Variables de entorno requeridas

```
SECRET_KEY=
DEBUG=True
DATABASE_URL=postgresql://...   # producción
```

## Convenciones específicas

- Tenant model: `Empresa` — NO renombrar a `Organization`
- Request tenant: NO hay `request.tenant` ni `request.org` — cada vista resuelve su empresa
- Reportes: usar reportlab para PDF, openpyxl para Excel
- Deploy: PythonAnywhere (NO Render, NO Docker, NO DigitalOcean)
