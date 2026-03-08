# Guia: Exponer Django a un cliente con tunnel SSH

Esta guia explica paso a paso como hacer que tu proyecto Django sea accesible
desde internet para que un cliente lo pruebe, sin necesidad de un servidor de
produccion ni cuentas en servicios externos.

---

## Contexto: Como funciona un tunnel

Normalmente tu servidor Django solo escucha en `127.0.0.1` (tu propia maquina).
Un tunnel crea un puente entre una URL publica en internet y tu puerto local:

```
Cliente en internet
       |
       v
https://xxx.serveousercontent.com   <-- URL publica (serveo.net)
       |
       v  (tunnel SSH)
Tu maquina: localhost:8080           <-- Django corriendo aqui
```

El servicio **serveo.net** actua de intermediario. La conexion se hace via SSH,
que ya viene instalado en Linux/Mac, sin necesidad de instalar nada extra.

---

## Paso 1: Identificar en que puerto corre Django

Antes de crear el tunnel necesitas saber en que puerto esta corriendo tu
servidor Django. Ejecuta:

```bash
ps aux | grep "manage.py" | grep -v grep
```

La salida mostrara algo como:

```
sabh  101297  ...  python manage.py runserver 8080
```

El numero al final (`8080`, `8000`, `8090`, etc.) es tu puerto. Anotalo.

Si hay varios procesos Django corriendo, identifica cual corresponde a tu
proyecto buscando la ruta en la columna de comando.

---

## Paso 2: Configurar Django para aceptar el dominio del tunnel

Por seguridad, Django rechaza peticiones de dominios no autorizados. Hay dos
lugares donde debes agregar el dominio de serveo.

### 2a. Archivo `.env`

Abre el archivo `.env` en la raiz del proyecto y modifica `ALLOWED_HOSTS`:

```env
# Antes:
ALLOWED_HOSTS=localhost,127.0.0.1

# Despues:
ALLOWED_HOSTS=localhost,127.0.0.1,.serveousercontent.com
```

El punto al inicio de `.serveousercontent.com` le dice a Django que acepte
cualquier subdominio de ese dominio (ej: `abc123.serveousercontent.com`).

### 2b. Archivo `config/settings/development.py`

Agrega la variable `CSRF_TRUSTED_ORIGINS` para que los formularios funcionen
correctamente a traves del tunnel (Django 4+ lo requiere para HTTPS):

```python
# Al final del archivo:
CSRF_TRUSTED_ORIGINS = ['https://*.serveousercontent.com']
```

Sin esto, cualquier formulario (login, crear proyectos, etc.) dara error
403 Forbidden al enviarse desde la URL del tunnel.

### Por que Django recarga automaticamente

Django en modo desarrollo usa `StatReloader`, que detecta cambios en archivos
`.py` y `.env` y reinicia el servidor automaticamente. No necesitas reiniciarlo
manualmente al editar estos archivos.

---

## Paso 3: Crear el tunnel con serveo.net

Con Django corriendo, ejecuta este comando en tu terminal:

```bash
ssh -o StrictHostKeyChecking=no \
    -o ServerAliveInterval=30 \
    -o ServerAliveCountMax=3 \
    -R 80:localhost:8080 \
    serveo.net
```

Reemplaza `8080` con el puerto real de tu proyecto.

**Que hace cada opcion:**

| Opcion | Descripcion |
|--------|-------------|
| `StrictHostKeyChecking=no` | Acepta la clave SSH de serveo sin pedir confirmacion manual la primera vez |
| `ServerAliveInterval=30` | Envia un ping cada 30 segundos para mantener la conexion viva |
| `ServerAliveCountMax=3` | Si no responde 3 pings seguidos, cierra y permite reconectar |
| `-R 80:localhost:8080` | Reenviar el puerto 80 de serveo hacia tu localhost:8080 |

La salida sera algo como:

```
Forwarding HTTP traffic from https://014e1e04ea12d3f5-159-26-99-229.serveousercontent.com
```

Esa URL es la que le envias a tu cliente. Funciona inmediatamente desde
cualquier navegador sin que el cliente instale nada.

---

## Paso 4: Mantener el tunnel activo en segundo plano

Si cierras la terminal, el tunnel se cae. Para dejarlo corriendo en segundo
plano usa `nohup`:

```bash
nohup ssh -o StrictHostKeyChecking=no \
          -o ServerAliveInterval=30 \
          -o ServerAliveCountMax=3 \
          -R 80:localhost:8080 \
          serveo.net > /tmp/tunnel_smart_pm.log 2>&1 &

echo "Tunnel PID: $!"
```

Para ver la URL generada:

```bash
cat /tmp/tunnel_smart_pm.log
```

Para ver si sigue activo:

```bash
ps aux | grep serveo | grep -v grep
```

Para cerrarlo:

```bash
# Busca el PID
ps aux | grep serveo | grep -v grep

# Luego mata el proceso
kill <PID>
```

---

## Solucion de problemas comunes

### Error: "DisallowedHost"

```
Invalid HTTP_HOST header: 'xxx.serveousercontent.com'
```

**Causa:** Django no tiene el dominio en `ALLOWED_HOSTS`.

**Solucion:** Verifica que `.serveousercontent.com` este en el `.env` y que
Django haya recargado (si no recargo, reinicia el servidor manualmente).

---

### Error: El tunnel se cayo (pagina no carga)

**Causa:** La conexion SSH a serveo.net se interrumpio. Esto pasa si la maquina
estuvo inactiva o hay inestabilidad de red.

**Solucion:** Verifica con `ps aux | grep serveo | grep -v grep`. Si no aparece,
ejecuta de nuevo el comando del Paso 3. La nueva URL sera diferente, debes
enviarsela de nuevo al cliente.

---

### Error: El tunnel apunta al proyecto equivocado

Si tienes varios proyectos Django corriendo (en diferentes puertos), el tunnel
debe apuntar al puerto correcto. Verifica con:

```bash
ps aux | grep "manage.py" | grep -v grep
```

Y ajusta el numero de puerto en el comando SSH.

---

### El formulario de login da error 403

**Causa:** Falta `CSRF_TRUSTED_ORIGINS` en `development.py`.

**Solucion:** Agrega la linea del Paso 2b y espera a que Django recargue.

---

## Limitaciones de serveo.net

- La URL cambia cada vez que el tunnel se reinicia (no es fija).
- Es un servicio gratuito sin garantia de disponibilidad.
- No recomendado para produccion, solo para demostraciones rapidas.

---

## Alternativa: localtunnel con URL personalizada

Si necesitas una URL mas predecible (aunque no garantizada):

```bash
npx localtunnel --port 8080 --subdomain mi-smart-pm
```

Esto genera `https://mi-smart-pm.loca.lt`. Requiere `node` instalado.

Agrega `loca.lt` a la configuracion de Django:

```env
ALLOWED_HOSTS=localhost,127.0.0.1,.serveousercontent.com,.loca.lt
```

```python
CSRF_TRUSTED_ORIGINS = [
    'https://*.serveousercontent.com',
    'https://*.loca.lt',
]
```

**Nota:** localtunnel muestra una pantalla de advertencia al cliente la primera
vez que accede. Debe ingresar su IP publica para continuar.

---

## Resumen rapido (comandos del dia a dia)

```bash
# 1. Verificar que Django corre y en que puerto
ps aux | grep "manage.py" | grep -v grep

# 2. Crear tunnel (reemplaza 8080 con tu puerto)
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -R 80:localhost:8080 serveo.net

# 3. Si se cae, verificar y reiniciar
ps aux | grep serveo | grep -v grep
# Si no aparece, ejecutar el comando de arriba de nuevo

# 4. Ver logs del tunnel en background
cat /tmp/tunnel_smart_pm.log
```
