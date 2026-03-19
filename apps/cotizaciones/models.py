"""
Sistema de Cotizaciones.
"""
import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from apps.core.models import Empresa, Usuario
from apps.bd_costos.models import ItemCosto


class Cotizacion(models.Model):
    """
    Presupuesto/propuesta comercial para un cliente.
    """
    ESTADO_BORRADOR = 'BORRADOR'
    ESTADO_ENVIADA = 'ENVIADA'
    ESTADO_APROBADA = 'APROBADA'
    ESTADO_RECHAZADA = 'RECHAZADA'
    ESTADO_VENCIDA = 'VENCIDA'
    ESTADO_CONVERTIDA = 'CONVERTIDA'

    ESTADOS = [
        (ESTADO_BORRADOR, 'Borrador'),
        (ESTADO_ENVIADA, 'Enviada'),
        (ESTADO_APROBADA, 'Aprobada'),
        (ESTADO_RECHAZADA, 'Rechazada'),
        (ESTADO_VENCIDA, 'Vencida'),
        (ESTADO_CONVERTIDA, 'Convertida a proyecto'),
    ]

    ESTADOS_COLOR = {
        ESTADO_BORRADOR: 'gray',
        ESTADO_ENVIADA: 'blue',
        ESTADO_APROBADA: 'green',
        ESTADO_RECHAZADA: 'red',
        ESTADO_VENCIDA: 'yellow',
        ESTADO_CONVERTIDA: 'purple',
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='cotizaciones')
    numero = models.CharField('Número', max_length=20, unique=True)

    # Activo asociado (opcional)
    activo_cliente = models.ForeignKey(
        'activos.ActivoCliente',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='cotizaciones',
        verbose_name='Equipo/Activo asociado'
    )

    # Datos del cliente
    cliente_nombre = models.CharField('Nombre del cliente', max_length=200)
    cliente_rif = models.CharField('RIF del cliente', max_length=15, blank=True)
    cliente_direccion = models.TextField('Dirección del cliente', blank=True)
    cliente_telefono = models.CharField('Teléfono del cliente', max_length=20, blank=True)
    cliente_email = models.EmailField('Email del cliente', blank=True)
    cliente_contacto = models.CharField('Persona de contacto', max_length=100, blank=True)

    # Datos del proyecto
    nombre_proyecto = models.CharField('Nombre del proyecto', max_length=200)
    descripcion = models.TextField('Descripción del alcance')
    ubicacion = models.CharField('Ubicación', max_length=200, blank=True)

    # Estado y fechas
    estado = models.CharField('Estado', max_length=20, choices=ESTADOS, default=ESTADO_BORRADOR)
    fecha_creacion = models.DateField('Fecha de creación', auto_now_add=True)
    fecha_vencimiento = models.DateField('Válida hasta')
    fecha_envio = models.DateTimeField('Fecha de envío', null=True, blank=True)
    fecha_respuesta = models.DateTimeField('Fecha de respuesta', null=True, blank=True)

    # Financiero
    moneda = models.CharField('Moneda', max_length=3, default='USD')
    subtotal = models.DecimalField('Subtotal', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    margen_utilidad_porcentaje = models.DecimalField(
        'Margen de utilidad (%)', max_digits=5, decimal_places=2, default=Decimal('15.00')
    )
    utilidad_monto = models.DecimalField('Utilidad', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))

    # Términos y notas
    terminos_condiciones = models.TextField('Términos y condiciones', blank=True)
    notas_internas = models.TextField('Notas internas (no visible al cliente)', blank=True)
    observaciones_cliente = models.TextField('Observaciones del cliente', blank=True)

    # Auditoría
    creado_por = models.ForeignKey(
        Usuario, on_delete=models.PROTECT,
        related_name='cotizaciones_creadas', verbose_name='Creado por'
    )
    modificado_por = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='cotizaciones_modificadas', verbose_name='Modificado por'
    )
    fecha_modificacion = models.DateTimeField('Última modificación', auto_now=True)

    class Meta:
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['empresa', 'estado']),
            models.Index(fields=['empresa', 'fecha_creacion']),
        ]

    def __str__(self):
        return f"{self.numero} — {self.nombre_proyecto} ({self.cliente_nombre})"

    @property
    def estado_color(self):
        return self.ESTADOS_COLOR.get(self.estado, 'gray')

    @property
    def puede_editarse(self):
        return self.estado in (self.ESTADO_BORRADOR, self.ESTADO_ENVIADA)

    @property
    def esta_vencida(self):
        from datetime import date
        return (
            self.estado not in (self.ESTADO_APROBADA, self.ESTADO_CONVERTIDA, self.ESTADO_RECHAZADA)
            and self.fecha_vencimiento < date.today()
        )

    def calcular_totales(self):
        """Recalcula subtotal, utilidad y total desde las partidas."""
        self.subtotal = sum(p.subtotal for p in self.partidas.all())
        self.utilidad_monto = (self.subtotal * self.margen_utilidad_porcentaje / Decimal('100')).quantize(Decimal('0.01'))
        self.total = self.subtotal + self.utilidad_monto

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self._generar_numero()
        if not self.terminos_condiciones and self.empresa_id:
            self.terminos_condiciones = self.empresa.terminos_condiciones_default
        super().save(*args, **kwargs)

    def _generar_numero(self):
        from datetime import date
        año = date.today().year
        ultimo = Cotizacion.objects.filter(
            empresa=self.empresa,
            numero__startswith=f'COT-{año}-'
        ).count()
        return f'COT-{año}-{str(ultimo + 1).zfill(3)}'


class PartidaCotizacion(models.Model):
    """
    Línea individual de trabajo/material en una cotización.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='partidas')
    orden = models.PositiveSmallIntegerField('Orden', default=0)

    # Referencia opcional a BD de costos
    item_costo = models.ForeignKey(
        ItemCosto, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='partidas_cotizacion', verbose_name='Ítem de BD de costos'
    )

    # Campos copiados/editables
    codigo = models.CharField('Código', max_length=30, blank=True)
    descripcion = models.CharField('Descripción', max_length=300)
    unidad = models.CharField('Unidad', max_length=20)
    categoria = models.CharField('Categoría/Sección', max_length=100, blank=True)
    cantidad = models.DecimalField('Cantidad', max_digits=12, decimal_places=4)
    precio_unitario = models.DecimalField('Precio unitario', max_digits=12, decimal_places=4)
    subtotal = models.DecimalField('Subtotal', max_digits=14, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = 'Partida de cotización'
        verbose_name_plural = 'Partidas de cotización'
        ordering = ['orden']

    def __str__(self):
        return f"{self.codigo or '—'} {self.descripcion} ({self.cotizacion.numero})"

    def save(self, *args, **kwargs):
        self.subtotal = (self.cantidad * self.precio_unitario).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
        # Recalcular totales de la cotización
        self.cotizacion.calcular_totales()
        self.cotizacion.save(update_fields=['subtotal', 'utilidad_monto', 'total'])
