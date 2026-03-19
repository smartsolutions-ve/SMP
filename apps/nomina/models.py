"""
Nómina y Horas Hombre — Gestión de cargos, costos HH y registros de horas.
"""
import uuid
from decimal import Decimal
from django.db import models
from apps.core.models import Empresa, Usuario


class CargoTrabajador(models.Model):
    """
    Cargo o rol de trabajador con su costo por hora.
    Se sincroniza opcionalmente con BD de Costos como ítem tipo MANO_OBRA.
    """
    NIVEL_CHOICES = [
        ('AYUDANTE', 'Ayudante'),
        ('OFICIAL', 'Oficial'),
        ('MAESTRO', 'Maestro'),
        ('ESPECIALISTA', 'Especialista'),
        ('SUPERVISOR', 'Supervisor'),
        ('INGENIERO', 'Ingeniero'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='cargos')

    codigo = models.CharField('Código', max_length=20)
    nombre = models.CharField('Nombre del cargo', max_length=100)
    nivel = models.CharField('Nivel', max_length=20, choices=NIVEL_CHOICES, default='OFICIAL')
    descripcion = models.TextField('Descripción', blank=True)

    # Costo
    costo_hora = models.DecimalField('Costo por hora ($)', max_digits=10, decimal_places=2)
    moneda = models.CharField('Moneda', max_length=3, default='USD')

    # Sincronización con BD de Costos
    item_costo = models.OneToOneField(
        'bd_costos.ItemCosto',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='cargo_origen',
        verbose_name='Ítem en BD de Costos',
        help_text='Ítem de mano de obra vinculado en la BD de costos'
    )

    activo = models.BooleanField('Activo', default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cargo de trabajador'
        verbose_name_plural = 'Cargos de trabajadores'
        ordering = ['nivel', 'nombre']
        unique_together = [('empresa', 'codigo')]

    def __str__(self):
        return f"{self.codigo} — {self.nombre} (${self.costo_hora}/h)"

    def sincronizar_item_costo(self):
        """Crea o actualiza el ítem correspondiente en BD de Costos."""
        from apps.bd_costos.models import ItemCosto, HistorialPrecio

        if self.item_costo:
            # Actualizar existente
            item = self.item_costo
            precio_anterior = item.precio_actual
            item.descripcion = f"{self.nombre} (HH)"
            item.precio_actual = self.costo_hora
            item.moneda = self.moneda
            item.save()
            if precio_anterior != self.costo_hora:
                HistorialPrecio.objects.create(
                    item=item,
                    precio=precio_anterior,
                    moneda=self.moneda,
                    observacion=f'Actualización desde Nómina: {self.nombre}',
                    usuario=None,
                )
        else:
            # Crear nuevo
            item = ItemCosto.objects.create(
                empresa=self.empresa,
                codigo=f"HH-{self.codigo}",
                descripcion=f"{self.nombre} (HH)",
                tipo='MANO_OBRA',
                unidad='h',
                precio_actual=self.costo_hora,
                moneda=self.moneda,
                creado_por=None,
            )
            self.item_costo = item
            self.save(update_fields=['item_costo'])
            HistorialPrecio.objects.create(
                item=item,
                precio=self.costo_hora,
                moneda=self.moneda,
                observacion=f'Creado desde Nómina: {self.nombre}',
                usuario=None,
            )


class HistorialCostoHH(models.Model):
    """Registro inmutable de cambios en el costo por hora de un cargo."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cargo = models.ForeignKey(CargoTrabajador, on_delete=models.CASCADE, related_name='historial')
    costo_hora_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    costo_hora_nuevo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.CharField(max_length=200, blank=True)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='cambios_costo_hh'
    )

    class Meta:
        verbose_name = 'Historial de costo HH'
        verbose_name_plural = 'Historial de costos HH'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.cargo.nombre}: ${self.costo_hora_anterior} → ${self.costo_hora_nuevo}"


class RegistroHH(models.Model):
    """
    Registro de horas hombre trabajadas en una partida de proyecto.
    Inmutable una vez creado.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partida = models.ForeignKey(
        'proyectos.PartidaProyecto',
        on_delete=models.PROTECT,
        related_name='registros_hh',
        verbose_name='Partida del proyecto'
    )
    cargo = models.ForeignKey(
        CargoTrabajador,
        on_delete=models.PROTECT,
        related_name='registros_hh',
        verbose_name='Cargo'
    )

    fecha = models.DateField('Fecha')
    cantidad_trabajadores = models.PositiveSmallIntegerField('Cantidad de trabajadores', default=1)
    horas = models.DecimalField('Horas trabajadas', max_digits=6, decimal_places=2)
    costo_hora_aplicado = models.DecimalField(
        'Costo/hora aplicado', max_digits=10, decimal_places=2,
        help_text='Snapshot del costo al momento del registro'
    )
    costo_total = models.DecimalField('Costo total HH', max_digits=12, decimal_places=2)
    observaciones = models.TextField('Observaciones', blank=True)

    registrado_por = models.ForeignKey(
        Usuario, on_delete=models.PROTECT,
        related_name='registros_hh', verbose_name='Registrado por'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Registro de horas hombre'
        verbose_name_plural = 'Registros de horas hombre'
        ordering = ['-fecha', '-fecha_registro']

    def __str__(self):
        return f"{self.cargo.nombre} — {self.horas}h — {self.fecha}"

    def save(self, *args, **kwargs):
        # Calcular costo total: trabajadores × horas × costo/hora
        self.costo_total = (
            Decimal(str(self.cantidad_trabajadores)) * self.horas * self.costo_hora_aplicado
        ).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)

    @property
    def total_hh(self):
        """Total horas hombre = trabajadores × horas."""
        return self.cantidad_trabajadores * self.horas
