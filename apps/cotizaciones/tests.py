from django.test import TestCase
import datetime
from decimal import Decimal
from apps.core.models import Empresa, Usuario
from apps.cotizaciones.models import Cotizacion, PartidaCotizacion

class CotizacionFinancieraTests(TestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nombre="Empresa Test",
            rif="J-12345678-9",
            margen_utilidad_default=Decimal('10.00')
        )
        self.user = Usuario.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword',
            empresa=self.empresa
        )
        self.cotizacion = Cotizacion.objects.create(
            empresa=self.empresa,
            creado_por=self.user,
            cliente_nombre="Cliente Prueba",
            descripcion="Prueba",
            fecha_vencimiento=datetime.date.today() + datetime.timedelta(days=15),
            margen_utilidad_porcentaje=Decimal('15.00')
        )

    def test_recalculo_totales(self):
        PartidaCotizacion.objects.create(
            cotizacion=self.cotizacion,
            descripcion="Item 1",
            cantidad=Decimal('2.00'),
            precio_unitario=Decimal('100.00'),
            orden=1
        )
        self.cotizacion.refresh_from_db()
        self.assertEqual(self.cotizacion.subtotal, Decimal('200.00'))
        self.assertEqual(self.cotizacion.utilidad_monto, Decimal('30.00'))
        self.assertEqual(self.cotizacion.total, Decimal('230.00'))

        PartidaCotizacion.objects.create(
            cotizacion=self.cotizacion,
            descripcion="Item 2",
            cantidad=Decimal('1.00'),
            precio_unitario=Decimal('50.00'),
            orden=2
        )
        self.cotizacion.refresh_from_db()
        self.assertEqual(self.cotizacion.subtotal, Decimal('250.00'))
        self.assertEqual(self.cotizacion.utilidad_monto, Decimal('37.50'))
        self.assertEqual(self.cotizacion.total, Decimal('287.50'))
