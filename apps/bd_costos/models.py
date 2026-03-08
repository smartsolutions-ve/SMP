"""
Base de Datos de Costos.
Repositorio central de precios de materiales, mano de obra, equipos y subcontratos.
"""
import uuid
from django.db import models
from apps.core.models import Empresa, Usuario


class CategoriaItem(models.Model):
    """
    Organización jerárquica de ítems de costo.
    Máximo 3 niveles de profundidad.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='categorias_costo')
    nombre = models.CharField('Nombre', max_length=100)
    codigo = models.CharField('Código', max_length=20)
    padre = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='subcategorias',
        verbose_name='Categoría padre'
    )
    descripcion = models.TextField('Descripción', blank=True)
    activo = models.BooleanField('Activo', default=True)
    orden = models.PositiveSmallIntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Categoría de ítem'
        verbose_name_plural = 'Categorías de ítems'
        ordering = ['orden', 'codigo', 'nombre']
        unique_together = [('empresa', 'codigo')]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def nombre_jerarquico(self):
        if self.padre:
            return f"{self.padre.nombre_jerarquico} > {self.nombre}"
        return self.nombre


class ItemCosto(models.Model):
    """
    Ítem individual en la base de datos de costos.
    """
    TIPO_MATERIAL = 'MATERIAL'
    TIPO_MANO_OBRA = 'MANO_OBRA'
    TIPO_EQUIPO = 'EQUIPO'
    TIPO_SUBCONTRATO = 'SUBCONTRATO'
    TIPO_OTROS = 'OTROS'

    TIPOS = [
        (TIPO_MATERIAL, 'Material'),
        (TIPO_MANO_OBRA, 'Mano de Obra'),
        (TIPO_EQUIPO, 'Equipo/Maquinaria'),
        (TIPO_SUBCONTRATO, 'Subcontrato'),
        (TIPO_OTROS, 'Otros'),
    ]

    UNIDADES = [
        ('m2', 'm²'),
        ('m3', 'm³'),
        ('ml', 'ml (metro lineal)'),
        ('kg', 'kg'),
        ('ton', 'Tonelada'),
        ('un', 'Unidad'),
        ('lote', 'Lote'),
        ('dia', 'Día'),
        ('hora', 'Hora'),
        ('mes', 'Mes'),
        ('pie', 'Pie'),
        ('pulg', 'Pulgada'),
        ('otro', 'Otra'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='items_costo')
    codigo = models.CharField('Código', max_length=30)
    descripcion = models.CharField('Descripción', max_length=300)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPOS, default=TIPO_MATERIAL)
    categoria = models.ForeignKey(
        CategoriaItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items',
        verbose_name='Categoría'
    )
    unidad = models.CharField('Unidad', max_length=10, choices=UNIDADES, default='un')
    unidad_custom = models.CharField('Unidad personalizada', max_length=20, blank=True)

    precio_actual = models.DecimalField('Precio actual', max_digits=12, decimal_places=4)
    moneda = models.CharField('Moneda', max_length=3, choices=[('USD', 'USD'), ('VES', 'VES')], default='USD')
    fecha_actualizacion = models.DateField('Última actualización', auto_now=True)

    especificaciones = models.TextField('Especificaciones técnicas', blank=True)
    proveedor_preferido = models.CharField('Proveedor preferido', max_length=150, blank=True)
    notas = models.TextField('Notas internas', blank=True)

    activo = models.BooleanField('Activo', default=True)
    creado_por = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True,
        related_name='items_creados', verbose_name='Creado por'
    )
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)

    class Meta:
        verbose_name = 'Ítem de costo'
        verbose_name_plural = 'Ítems de costo'
        ordering = ['tipo', 'codigo']
        unique_together = [('empresa', 'codigo')]
        indexes = [
            models.Index(fields=['empresa', 'tipo']),
            models.Index(fields=['empresa', 'descripcion']),
        ]

    def __str__(self):
        return f"[{self.codigo}] {self.descripcion}"

    @property
    def unidad_display(self):
        if self.unidad == 'otro':
            return self.unidad_custom
        return self.get_unidad_display()


class HistorialPrecio(models.Model):
    """
    Histórico de cambios de precio de un ítem.
    Registro inmutable (no se edita ni elimina).
    """
    item = models.ForeignKey(ItemCosto, on_delete=models.CASCADE, related_name='historial_precios')
    fecha = models.DateField('Fecha del cambio', auto_now_add=True)
    precio = models.DecimalField('Precio', max_digits=12, decimal_places=4)
    moneda = models.CharField('Moneda', max_length=3)
    observacion = models.CharField('Observación', max_length=200, blank=True)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True,
        related_name='cambios_precio', verbose_name='Registrado por'
    )

    class Meta:
        verbose_name = 'Historial de precio'
        verbose_name_plural = 'Historial de precios'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.item.codigo} — {self.precio} {self.moneda} ({self.fecha})"
