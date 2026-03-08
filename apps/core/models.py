"""
Modelos base del sistema: Empresa (tenant) y Usuario.
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Empresa(models.Model):
    """
    Entidad raíz del sistema multi-tenant.
    Representa cada empresa cliente del SaaS.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField('Razón Social', max_length=200)
    nombre_comercial = models.CharField('Nombre Comercial', max_length=200, blank=True)
    rif = models.CharField(
        'RIF',
        max_length=15,
        unique=True,
    )
    direccion = models.TextField('Dirección', blank=True)
    telefono = models.CharField('Teléfono', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)
    sitio_web = models.URLField('Sitio Web', blank=True)
    logo = models.ImageField('Logo', upload_to='logos/', null=True, blank=True)

    # Configuración operativa
    moneda_default = models.CharField(
        'Moneda por defecto',
        max_length=3,
        choices=[('USD', 'Dólares (USD)'), ('VES', 'Bolívares (VES)')],
        default='USD'
    )
    margen_utilidad_default = models.DecimalField(
        'Margen de utilidad (%)',
        max_digits=5,
        decimal_places=2,
        default=15.00
    )
    terminos_condiciones_default = models.TextField(
        'Términos y condiciones',
        blank=True,
        default=(
            "VALIDEZ DE LA OFERTA: 15 días calendario\n\n"
            "FORMA DE PAGO:\n"
            "- 30% anticipo contra firma de contrato\n"
            "- 40% contra avance de obra\n"
            "- 30% contraentrega y recepción final\n\n"
            "GARANTÍA: 100 días contra defectos de ejecución\n\n"
            "NO INCLUYE:\n"
            "- Permisos y tramitología\n"
            "- Estudios técnicos adicionales"
        )
    )

    activo = models.BooleanField('Activo', default=True)
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.rif})"

    @property
    def nombre_display(self):
        return self.nombre_comercial or self.nombre


class Usuario(AbstractUser):
    """
    Usuario extendido. Pertenece a una empresa.
    """
    ROL_ADMIN = 'ADMIN'
    ROL_GERENTE = 'GERENTE'
    ROL_SUPERVISOR = 'SUPERVISOR'
    ROL_CLIENTE = 'CLIENTE'

    ROLES = [
        (ROL_ADMIN, 'Administrador'),
        (ROL_GERENTE, 'Gerente'),
        (ROL_SUPERVISOR, 'Supervisor'),
        (ROL_CLIENTE, 'Cliente (externo)'),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        related_name='usuarios',
        null=True,
        blank=True,
        verbose_name='Empresa'
    )
    rol = models.CharField('Rol', max_length=20, choices=ROLES, default=ROL_GERENTE)
    telefono = models.CharField('Teléfono', max_length=20, blank=True)
    foto_perfil = models.ImageField('Foto de perfil', upload_to='perfiles/', null=True, blank=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"

    @property
    def es_admin(self):
        return self.rol == self.ROL_ADMIN

    @property
    def es_gerente_o_superior(self):
        return self.rol in (self.ROL_ADMIN, self.ROL_GERENTE)

    @property
    def puede_ver_costos(self):
        """Supervisores NO ven costos."""
        return self.rol != self.ROL_SUPERVISOR

    @property
    def puede_editar_cotizaciones(self):
        return self.rol in (self.ROL_ADMIN, self.ROL_GERENTE)

    @property
    def puede_aprobar_cambios(self):
        return self.rol in (self.ROL_ADMIN, self.ROL_GERENTE)
