# Guia de Despliegue en PythonAnywhere (via GitHub)

**Proyecto:** Smart Project Management
**Fecha:** 2026-03-07
**Tiempo estimado:** 30-45 minutos

---

## Antes de empezar — Genera una SECRET_KEY segura

Ejecuta esto en tu terminal local y guarda el resultado:

```bash
cd "/home/sabh/Documentos/Smart/Smart Project Management" && source env/bin/activate
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Parte A — Preparar el repositorio GitHub (solo la primera vez)

### A1. Inicializar git en el proyecto

En tu terminal local:

```bash
cd "/home/sabh/Documentos/Smart/Smart Project Management/smart_pm"
git init
git add .
git status    # verifica que .env y db.sqlite3 NO aparezcan en la lista
```

Si `db.sqlite3` o `.env` aparecen en la lista, el `.gitignore` no esta funcionando.
Verifica que el archivo `.gitignore` existe en la raiz del proyecto.

### A2. Crear el repositorio en GitHub

1. Ve a [github.com](https://github.com) e inicia sesion
2. Clic en **"New repository"** (boton verde)
3. Nombre: `smart-pm` (o `smart_project_management`)
4. Visibilidad: **Private** (importante — el codigo de clientes es privado)
5. NO marques "Initialize this repository" (ya tienes codigo)
6. Clic en **"Create repository"**

### A3. Conectar y subir el codigo

GitHub te mostrara los comandos. Usa estos:

```bash
cd "/home/sabh/Documentos/Smart/Smart Project Management/smart_pm"
git remote add origin https://github.com/TU_USUARIO_GITHUB/smart-pm.git
git branch -M main
git commit -m "Initial commit: MVP Smart Project Management"
git push -u origin main
```

Verifica en GitHub que los archivos subieron y que **NO hay** `.env` ni `db.sqlite3`.

---

## Parte B — Despliegue en PythonAnywhere

### Paso 1 — Crear cuenta en PythonAnywhere

1. Ve a [pythonanywhere.com](https://www.pythonanywhere.com)
2. Clic en **"Start running Python online in less than a minute"**
3. Elige **Beginner account** (gratuita)
4. Registrate y confirma el email

Tu URL publica quedara: `https://TU_USUARIO_PA.pythonanywhere.com`

---

### Paso 2 — Clonar el repositorio

1. En el dashboard de PythonAnywhere, ve a la pestana **Consoles**
2. Clic en **"Bash"**

```bash
cd ~
git clone https://github.com/TU_USUARIO_GITHUB/smart-pm.git smart_pm
ls smart_pm/    # debes ver: apps/ config/ templates/ manage.py etc.
```

Si el repositorio es privado, GitHub te pedira usuario y password.
Para repositorios privados se recomienda usar un **Personal Access Token**:

1. En GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Genera un token con permiso `repo`
3. Usa ese token como password al clonar

---

### Paso 3 — Crear el entorno virtual e instalar dependencias

```bash
python3.13 -m venv ~/smart_pm_env
source ~/smart_pm_env/bin/activate
pip install --upgrade pip
pip install -r ~/smart_pm/requirements/pythonanywhere.txt
```

Verifica que Django se instalo:

```bash
python -c "import django; print(django.__version__)"
# Debe mostrar: 6.0.3
```

---

### Paso 4 — Crear el archivo .env

El `.env` no esta en GitHub por seguridad. Crealo manualmente:

```bash
nano ~/smart_pm/.env
```

Contenido (reemplaza los valores `< >`):

```env
SECRET_KEY=<pega-la-clave-generada-antes-del-despliegue>
DEBUG=False
ALLOWED_HOSTS=<TU_USUARIO_PA>.pythonanywhere.com

# SQLite en PythonAnywhere free (no requiere PostgreSQL)
USE_SQLITE=True
```

Guarda: `Ctrl+O` → `Enter` → `Ctrl+X`

---

### Paso 5 — Verificar que Django arranca

```bash
cd ~/smart_pm
source ~/smart_pm_env/bin/activate
DJANGO_SETTINGS_MODULE=config.settings.pythonanywhere python manage.py check
```

Resultado esperado: `System check identified no issues (0 silenced).`

---

### Paso 6 — Inicializar la base de datos

```bash
# Crear todas las tablas
DJANGO_SETTINGS_MODULE=config.settings.pythonanywhere python manage.py migrate

# Recolectar archivos estaticos (CSS, JS, imagenes)
DJANGO_SETTINGS_MODULE=config.settings.pythonanywhere python manage.py collectstatic --noinput

# Crear superusuario administrador
DJANGO_SETTINGS_MODULE=config.settings.pythonanywhere python manage.py createsuperuser
```

En `createsuperuser` pon:
- Username: `admin`
- Email: tu email
- Password: una contrasena segura

---

### Paso 7 — Configurar la aplicacion web en el dashboard

1. Dashboard > pestana **Web** > **"Add a new web app"**
2. **Next** → **"Manual configuration"** → **Python 3.13** → **Next**

Ahora estas en la pagina de configuracion. Hay 3 cosas a configurar:

#### 7a. Archivo WSGI

Busca la seccion **"Code"** y haz clic en el enlace del archivo WSGI
(algo como `/var/www/TU_USUARIO_PA_pythonanywhere_com_wsgi.py`)

Borra todo el contenido y reemplaza con:

```python
import sys
import os

# Ruta al directorio del proyecto (donde esta manage.py)
path = '/home/TU_USUARIO_PA/smart_pm'
if path not in sys.path:
    sys.path.insert(0, path)

# Settings de PythonAnywhere
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.pythonanywhere'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Reemplaza `TU_USUARIO_PA` con tu usuario de PythonAnywhere. Guarda.

#### 7b. Entorno virtual

En la seccion **"Virtualenv"**:
- Escribe: `/home/TU_USUARIO_PA/smart_pm_env`
- Clic en el check para confirmar

#### 7c. Archivos estaticos

En la seccion **"Static files"**, agrega dos entradas:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/TU_USUARIO_PA/smart_pm/staticfiles/` |
| `/media/` | `/home/TU_USUARIO_PA/smart_pm/media/` |

---

### Paso 8 — Recargar y probar

Clic en el boton verde **"Reload TU_USUARIO_PA.pythonanywhere.com"**

Visita: `https://TU_USUARIO_PA.pythonanywhere.com`

Debes ver el login de Smart Project Management.

---

### Paso 9 — Crear el tenant del cliente (Valmore)

1. Ve a `/admin/` e inicia sesion con el superusuario
2. **Empresas** > **Agregar empresa**:

| Campo | Valor |
|-------|-------|
| Nombre | Industrias Tecnicas Barquisimeto, C.A. |
| Nombre Comercial | I.T.B.C.A. |
| RIF | J-30803985-3 |
| Moneda default | USD |
| Margen utilidad default | 15.00 |

3. **Usuarios** > **Agregar usuario**:

| Campo | Valor |
|-------|-------|
| Username | valmore |
| Password | (una segura — la que le daras a el) |
| Empresa | Industrias Tecnicas Barquisimeto |
| Rol | ADMIN |
| First name | Valmore |

4. Prueba el login con las credenciales de Valmore.
   Si ves el dashboard → despliegue exitoso.

---

## Parte C — Actualizaciones futuras (flujo normal)

Cuando hagas cambios en el codigo y quieras actualizar el servidor:

### En tu maquina local:

```bash
cd "/home/sabh/Documentos/Smart/Smart Project Management/smart_pm"
git add .
git commit -m "descripcion del cambio"
git push origin main
```

### En PythonAnywhere (consola Bash):

```bash
cd ~/smart_pm
git pull origin main

# Solo si hay cambios en modelos de datos:
source ~/smart_pm_env/bin/activate
DJANGO_SETTINGS_MODULE=config.settings.pythonanywhere python manage.py migrate

# Solo si hay cambios en archivos estaticos:
DJANGO_SETTINGS_MODULE=config.settings.pythonanywhere python manage.py collectstatic --noinput
```

Luego en el dashboard > **Web** > clic en **"Reload"**.

---

## Solucion de problemas comunes

### Error 500 al entrar al sitio

Dashboard > **Web** > **"Error log"** — lee la ultima linea del error.

**Error mas comun:** `ModuleNotFoundError: No module named 'config'`
→ El path en el WSGI esta mal. Verifica que apunte exactamente a donde esta `manage.py`.

### Los estilos no cargan (sitio sin CSS)

1. Verifica que corriste `collectstatic`
2. Verifica que la URL en Static files es `/static/` (con barra final)
3. Verifica que el directorio es `staticfiles/` no `static/`

### "DisallowedHost at /"

El `ALLOWED_HOSTS` en `.env` no coincide con el dominio.
Debe ser exactamente: `tuusuario.pythonanywhere.com` (sin https://, sin barras)

### "Invalid HTTP_HOST header" despues de recargar

Edita el `.env` en PythonAnywhere y verifica el valor de `ALLOWED_HOSTS`.
Recarga la app despues de editar el `.env`.

### Las fotos subidas no se ven

```bash
mkdir -p ~/smart_pm/media
```
Y verifica que la entrada de `/media/` este en la seccion Static files del dashboard.

### GitHub pide contrasena al hacer git pull

El token expiro o no fue guardado. Vuelve a configurar:

```bash
git remote set-url origin https://TU_TOKEN@github.com/TU_USUARIO_GITHUB/smart-pm.git
```

---

## Resumen de rutas en PythonAnywhere

| Recurso | Ruta |
|---------|------|
| Codigo del proyecto | `/home/TU_USUARIO_PA/smart_pm/` |
| Entorno virtual | `/home/TU_USUARIO_PA/smart_pm_env/` |
| Archivo .env | `/home/TU_USUARIO_PA/smart_pm/.env` |
| Base de datos | `/home/TU_USUARIO_PA/smart_pm/db.sqlite3` |
| Estaticos compilados | `/home/TU_USUARIO_PA/smart_pm/staticfiles/` |
| Media (fotos) | `/home/TU_USUARIO_PA/smart_pm/media/` |
| Archivo WSGI | `/var/www/TU_USUARIO_PA_pythonanywhere_com_wsgi.py` |
| Logs de error | Dashboard > Web > Error log |
| URL publica | `https://TU_USUARIO_PA.pythonanywhere.com` |
