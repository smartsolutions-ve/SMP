"""
Gestión de Proyectos en Ejecución.
"""
import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from apps.core.models import Empresa, Usuario


class Proyecto(models.Model):
    """
    Proyecto en ejecución, normalmente convertido desde una cotización aprobada.
    """
    ESTADO_PLANIFICACION = 'PLANIFICACION'
    ESTADO_EN_EJECUCION = 'EN_EJECUCION'
    ESTADO_PAUSADO = 'PAUSADO'
    ESTADO_COMPLETADO = 'COMPLETADO'
    ESTADO_CANCELADO = 'CANCELADO'

    ESTADOS = [
        (ESTADO_PLANIFICACION, 'Planificación'),
        (ESTADO_EN_EJECUCION, 'En Ejecución'),
        (ESTADO_PAUSADO, 'Pausado'),
        (ESTADO_COMPLETADO, 'Completado'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='proyectos')

    # Referencia a cotización origen (opcional)
    cotizacion_origen = models.OneToOneField(
        'cotizaciones.Cotizacion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proyecto',
        verbose_name='Cotización de origen'
    )

    codigo = models.CharField('Código', max_length=20, unique=True)
    nombre = models.CharField('Nombre del proyecto', max_length=200)
    descripcion = models.TextField('Descripción', blank=True)
    ubicacion = models.CharField('Ubicación', max_length=200, blank=True)

    # Datos del cliente
    cliente_nombre = models.CharField('Cliente', max_length=200)
    cliente_rif = models.CharField('RIF del cliente', max_length=15, blank=True)
    cliente_contacto = models.CharField('Persona de contacto', max_length=100, blank=True)
    cliente_telefono = models.CharField('Teléfono del cliente', max_length=20, blank=True)
    cliente_email = models.EmailField('Email del cliente', blank=True)

    # Fechas
    fecha_inicio_planeada = models.DateField('Inicio planeado')
    fecha_inicio_real = models.DateField('Inicio real', null=True, blank=True)
    fecha_fin_planeada = models.DateField('Fin planeado')
    fecha_fin_real = models.DateField('Fin real', null=True, blank=True)

    # Financiero
    valor_contrato = models.DecimalField('Valor del contrato', max_digits=14, decimal_places=2)
    moneda = models.CharField('Moneda', max_length=3, default='USD')

    # Estado y avance
    estado = models.CharField('Estado', max_length=20, choices=ESTADOS, default=ESTADO_PLANIFICACION)
    porcentaje_avance = models.DecimalField(
        '% de avance', max_digits=5, decimal_places=2, default=Decimal('0.00')
    )

    # Equipo
    gerente_proyecto = models.ForeignKey(
        Usuario, on_delete=models.PROTECT,
        related_name='proyectos_como_gerente', verbose_name='Gerente de proyecto'
    )
    supervisor = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='proyectos_como_supervisor', verbose_name='Supervisor'
    )

    # Auditoría
    creado_por = models.ForeignKey(
        Usuario, on_delete=models.PROTECT,
        related_name='proyectos_creados', verbose_name='Creado por'
    )
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['empresa', 'estado']),
        ]

    def __str__(self):
        return f"{self.codigo} — {self.nombre}"

    @property
    def costo_real_total(self):
        return sum(p.costo_real for p in self.partidas.all()) or Decimal('0.00')

    @property
    def utilidad_real(self):
        return self.valor_contrato - self.costo_real_total

    @property
    def margen_real_porcentaje(self):
        if self.valor_contrato > 0:
            return (self.utilidad_real / self.valor_contrato * 100).quantize(Decimal('0.01'))
        return Decimal('0.00')

    @property
    def esta_atrasado(self):
        from datetime import date
        return (
            self.estado not in (self.ESTADO_COMPLETADO, self.ESTADO_CANCELADO)
            and self.fecha_fin_planeada < date.today()
        )

    @property
    def dias_transcurridos(self):
        from datetime import date
        inicio = self.fecha_inicio_real or self.fecha_inicio_planeada
        return (date.today() - inicio).days if inicio else 0

    @property
    def dias_restantes(self):
        from datetime import date
        return (self.fecha_fin_planeada - date.today()).days

    def recalcular_avance(self):
        """Promedio ponderado de avances por costo presupuestado."""
        partidas = list(self.partidas.all())
        total_presupuestado = sum(p.costo_presupuestado for p in partidas) or Decimal('1')
        avance = sum(
            p.porcentaje_avance * p.costo_presupuestado / total_presupuestado
            for p in partidas
        )
        self.porcentaje_avance = avance.quantize(Decimal('0.01'))
        self.save(update_fields=['porcentaje_avance'])

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self._generar_codigo()
        super().save(*args, **kwargs)

    def _generar_codigo(self):
        from datetime import date
        año = date.today().year
        ultimo = Proyecto.objects.filter(
            empresa=self.empresa,
            codigo__startswith=f'PROY-{año}-'
        ).count()
        return f'PROY-{año}-{str(ultimo + 1).zfill(3)}'


class PartidaProyecto(models.Model):
    """
    Línea de trabajo en ejecución real.
    """
    ESTADO_NO_INICIADA = 'NO_INICIADA'
    ESTADO_EN_PROCESO = 'EN_PROCESO'
    ESTADO_COMPLETADA = 'COMPLETADA'

    ESTADOS = [
        (ESTADO_NO_INICIADA, 'No iniciada'),
        (ESTADO_EN_PROCESO, 'En proceso'),
        (ESTADO_COMPLETADA, 'Completada'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='partidas')
    orden = models.PositiveSmallIntegerField('Orden', default=0)

    # Datos del presupuesto
    codigo = models.CharField('Código', max_length=30, blank=True)
    descripcion = models.CharField('Descripción', max_length=300)
    unidad = models.CharField('Unidad', max_length=20)
    categoria = models.CharField('Categoría/Sección', max_length=100, blank=True)
    cantidad_presupuestada = models.DecimalField('Cantidad presupuestada', max_digits=12, decimal_places=4)
    precio_unitario_presupuestado = models.DecimalField('P.U. presupuestado', max_digits=12, decimal_places=4)
    costo_presupuestado = models.DecimalField('Costo presupuestado', max_digits=14, decimal_places=2)

    # Datos de ejecución real
    cantidad_ejecutada = models.DecimalField('Cantidad ejecutada', max_digits=12, decimal_places=4, default=Decimal('0'))
    costo_real = models.DecimalField('Costo real', max_digits=14, decimal_places=2, default=Decimal('0.00'))

    # Estado y avance
    estado = models.CharField('Estado', max_length=20, choices=ESTADOS, default=ESTADO_NO_INICIADA)
    porcentaje_avance = models.DecimalField('% avance', max_digits=5, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = 'Partida del proyecto'
        verbose_name_plural = 'Partidas del proyecto'
        ordering = ['orden']

    def __str__(self):
        return f"{self.codigo or '—'} {self.descripcion}"

    @property
    def variacion_costo(self):
        return self.costo_real - self.costo_presupuestado

    @property
    def variacion_costo_porcentaje(self):
        if self.costo_presupuestado > 0:
            return (self.variacion_costo / self.costo_presupuestado * 100).quantize(Decimal('0.01'))
        return Decimal('0.00')

    def actualizar_desde_avance(self, cantidad_dia, costo_dia):
        """Llama esto al guardar un RegistroAvance."""
        self.cantidad_ejecutada += cantidad_dia
        self.costo_real += costo_dia

        if self.cantidad_presupuestada > 0:
            self.porcentaje_avance = min(
                (self.cantidad_ejecutada / self.cantidad_presupuestada * 100).quantize(Decimal('0.01')),
                Decimal('100.00')
            )
        else:
            self.porcentaje_avance = Decimal('0.00')

        # Actualizar estado automáticamente
        if self.porcentaje_avance >= 100:
            self.estado = self.ESTADO_COMPLETADA
        elif self.porcentaje_avance > 0:
            self.estado = self.ESTADO_EN_PROCESO
        else:
            self.estado = self.ESTADO_NO_INICIADA

        self.save()
        # Recalcular avance del proyecto
        self.proyecto.recalcular_avance()


class RegistroAvance(models.Model):
    """
    Registro diario del progreso de una partida.
    INMUTABLE: no se edita ni elimina una vez guardado.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partida = models.ForeignKey(PartidaProyecto, on_delete=models.PROTECT, related_name='registros')
    fecha = models.DateField('Fecha del avance')
    cantidad_ejecutada_dia = models.DecimalField('Cantidad ejecutada', max_digits=12, decimal_places=4)
    costo_dia = models.DecimalField('Costo del día', max_digits=12, decimal_places=2)
    observaciones = models.TextField('Observaciones', blank=True)
    registrado_por = models.ForeignKey(
        Usuario, on_delete=models.PROTECT,
        related_name='registros_avance', verbose_name='Registrado por'
    )
    fecha_registro = models.DateTimeField('Fecha de registro', auto_now_add=True)

    class Meta:
        verbose_name = 'Registro de avance'
        verbose_name_plural = 'Registros de avance'
        ordering = ['-fecha', '-fecha_registro']

    def __str__(self):
        return f"{self.partida.descripcion[:30]} — {self.fecha}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            # Actualizar la partida al guardar por primera vez
            self.partida.actualizar_desde_avance(
                self.cantidad_ejecutada_dia,
                self.costo_dia
            )


class FotoProyecto(models.Model):
    """
    Evidencia fotográfica del avance del proyecto.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='fotos')
    fecha = models.DateField('Fecha', auto_now_add=True)
    descripcion = models.CharField('Descripción', max_length=200)
    imagen = models.ImageField(
        'Imagen',
        upload_to='proyectos/%Y/%m/'
    )
    subido_por = models.ForeignKey(
        Usuario, on_delete=models.PROTECT,
        related_name='fotos_subidas', verbose_name='Subido por'
    )

    class Meta:
        verbose_name = 'Foto del proyecto'
        verbose_name_plural = 'Fotos del proyecto'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.proyecto.codigo} — {self.descripcion} ({self.fecha})"


class OrdenCambio(models.Model):
    """
    Cambio al alcance original del proyecto.
    """
    ESTADO_PENDIENTE = 'PENDIENTE'
    ESTADO_APROBADA = 'APROBADA'
    ESTADO_RECHAZADA = 'RECHAZADA'

    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente de aprobación'),
        (ESTADO_APROBADA, 'Aprobada'),
        (ESTADO_RECHAZADA, 'Rechazada'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='ordenes_cambio')
    numero = models.PositiveSmallIntegerField('N° de orden')
    fecha = models.DateField('Fecha', auto_now_add=True)

    descripcion = models.TextField('Descripción del cambio')
    justificacion = models.TextField('Justificación')
    impacto_costo = models.DecimalField('Impacto en costo ($)', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    impacto_tiempo_dias = models.IntegerField('Impacto en tiempo (días)', default=0)

    estado = models.CharField('Estado', max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    aprobado_por = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='ordenes_aprobadas', verbose_name='Aprobado por'
    )
    fecha_aprobacion = models.DateField('Fecha de aprobación', null=True, blank=True)
    observaciones_aprobacion = models.TextField('Observaciones de aprobación', blank=True)
    solicitado_por = models.ForeignKey(
        Usuario, on_delete=models.PROTECT,
        related_name='ordenes_solicitadas', verbose_name='Solicitado por'
    )

    class Meta:
        verbose_name = 'Orden de cambio'
        verbose_name_plural = 'Órdenes de cambio'
        ordering = ['numero']
        unique_together = [('proyecto', 'numero')]

    def __str__(self):
        return f"OC-{str(self.numero).zfill(3)} — {self.proyecto.codigo}"

    def aprobar(self, usuario, observaciones=''):
        """Aprueba la orden y actualiza el proyecto."""
        from datetime import date
        self.estado = self.ESTADO_APROBADA
        self.aprobado_por = usuario
        self.fecha_aprobacion = date.today()
        self.observaciones_aprobacion = observaciones
        self.save()

        # Actualizar contrato y fechas del proyecto
        if self.impacto_costo:
            self.proyecto.valor_contrato += self.impacto_costo
        if self.impacto_tiempo_dias:
            from datetime import timedelta
            self.proyecto.fecha_fin_planeada += timedelta(days=self.impacto_tiempo_dias)
        self.proyecto.save(update_fields=['valor_contrato', 'fecha_fin_planeada'])

    def rechazar(self, usuario, observaciones=''):
        """Rechaza la orden."""
        from datetime import date
        self.estado = self.ESTADO_RECHAZADA
        self.aprobado_por = usuario
        self.fecha_aprobacion = date.today()
        self.observaciones_aprobacion = observaciones
        self.save()
