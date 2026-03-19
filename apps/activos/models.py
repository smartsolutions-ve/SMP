"""
Activos del Cliente — Equipos y maquinaria registrada.
"""
import uuid
from django.db import models
from apps.core.models import Empresa, Usuario


class ActivoCliente(models.Model):
    """
    Equipo o activo registrado de un cliente.
    Permite asociar cotizaciones y proyectos a un equipo específico.
    """
    TIPO_CHOICES = [
        ('BOMBA', 'Bomba'),
        ('CALDERIN', 'Calderín'),
        ('TANQUE', 'Tanque'),
        ('TUBERIA', 'Tubería'),
        ('INTERCAMBIADOR', 'Intercambiador de calor'),
        ('COMPRESOR', 'Compresor'),
        ('MOTOR', 'Motor'),
        ('VALVULA', 'Válvula'),
        ('ESTRUCTURA', 'Estructura metálica'),
        ('OTRO', 'Otro'),
    ]

    ESTADO_CHOICES = [
        ('OPERATIVO', 'Operativo'),
        ('EN_REPARACION', 'En reparación'),
        ('FUERA_SERVICIO', 'Fuera de servicio'),
        ('RETIRADO', 'Retirado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='activos')

    # Identificación del equipo
    codigo_equipo = models.CharField('Código / TAG', max_length=50)
    nombre = models.CharField('Nombre del equipo', max_length=200)
    tipo = models.CharField('Tipo', max_length=30, choices=TIPO_CHOICES, default='OTRO')
    marca = models.CharField('Marca', max_length=100, blank=True)
    modelo = models.CharField('Modelo', max_length=100, blank=True)
    serial = models.CharField('Serial', max_length=100, blank=True)

    # Ubicación y cliente
    ubicacion = models.CharField('Ubicación / Planta', max_length=200, blank=True)
    area = models.CharField('Área / Sección', max_length=100, blank=True)
    cliente_nombre = models.CharField('Cliente propietario', max_length=200)
    cliente_rif = models.CharField('RIF del cliente', max_length=15, blank=True)

    # Estado y mantenimiento
    estado = models.CharField('Estado', max_length=20, choices=ESTADO_CHOICES, default='OPERATIVO')
    fecha_instalacion = models.DateField('Fecha de instalación', null=True, blank=True)
    frecuencia_mtto_dias = models.PositiveIntegerField(
        'Frecuencia de mtto. (días)', null=True, blank=True,
        help_text='Cada cuántos días requiere mantenimiento preventivo'
    )
    proximo_mtto = models.DateField('Próximo mantenimiento', null=True, blank=True)

    # Especificaciones técnicas
    especificaciones = models.TextField('Especificaciones técnicas', blank=True)
    notas = models.TextField('Notas', blank=True)

    # Auditoría
    activo = models.BooleanField('Activo', default=True)
    creado_por = models.ForeignKey(
        Usuario, on_delete=models.PROTECT,
        related_name='activos_creados', verbose_name='Creado por'
    )
    fecha_creacion = models.DateTimeField('Fecha de registro', auto_now_add=True)
    fecha_modificacion = models.DateTimeField('Última modificación', auto_now=True)

    class Meta:
        verbose_name = 'Activo del cliente'
        verbose_name_plural = 'Activos del cliente'
        ordering = ['cliente_nombre', 'codigo_equipo']
        indexes = [
            models.Index(fields=['empresa', 'cliente_nombre']),
            models.Index(fields=['empresa', 'tipo']),
        ]
        unique_together = [('empresa', 'codigo_equipo')]

    def __str__(self):
        return f"{self.codigo_equipo} — {self.nombre} ({self.cliente_nombre})"

    @property
    def estado_color(self):
        colores = {
            'OPERATIVO': 'green',
            'EN_REPARACION': 'yellow',
            'FUERA_SERVICIO': 'red',
            'RETIRADO': 'gray',
        }
        return colores.get(self.estado, 'gray')

    @property
    def requiere_mtto(self):
        """Verdadero si el próximo mantenimiento ya pasó o es hoy."""
        from datetime import date
        if self.proximo_mtto:
            return self.proximo_mtto <= date.today()
        return False

    @property
    def dias_para_mtto(self):
        from datetime import date
        if self.proximo_mtto:
            return (self.proximo_mtto - date.today()).days
        return None
