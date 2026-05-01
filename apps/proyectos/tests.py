from django.test import TestCase
from decimal import Decimal
import datetime
from apps.core.models import Empresa, Usuario
from apps.proyectos.models import Proyecto, PartidaProyecto, RegistroAvance

class ProyectoFinancieroTests(TestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nombre="Empresa Test",
            rif="J-12345678-9"
        )
        self.user = Usuario.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword',
            empresa=self.empresa
        )
        self.proyecto = Proyecto.objects.create(
            empresa=self.empresa,
            creado_por=self.user,
            gerente_proyecto=self.user,
            codigo="PRJ-001",
            nombre="Proyecto Financiero",
            cliente_nombre="Cliente X",
            valor_contrato=Decimal('1000.00'),
            fecha_inicio_planeada=datetime.date.today(),
            fecha_fin_planeada=datetime.date.today() + datetime.timedelta(days=30)
        )
        
        self.partida = PartidaProyecto.objects.create(
            proyecto=self.proyecto,
            codigo="P01",
            descripcion="Partida 1",
            unidad="un",
            cantidad_presupuestada=Decimal('10.00'),
            costo_presupuestado=Decimal('500.00'),
            precio_unitario_presupuestado=Decimal('50.00'),
            orden=1
        )

    def test_costo_y_utilidad(self):
        # Inicial: No hay avances reales
        self.assertEqual(self.proyecto.costo_real_total, Decimal('0.00'))
        self.assertEqual(self.proyecto.utilidad_real, Decimal('1000.00'))
        self.assertEqual(self.proyecto.margen_real_porcentaje, Decimal('100.00'))
        
        # Registramos avance
        RegistroAvance.objects.create(
            partida=self.partida,
            fecha=datetime.date.today(),
            cantidad_ejecutada_dia=Decimal('2.00'),
            costo_dia=Decimal('120.00'),
            registrado_por=self.user
        )
        
        self.assertEqual(self.proyecto.costo_real_total, Decimal('120.00'))
        self.assertEqual(self.proyecto.utilidad_real, Decimal('880.00'))
        self.assertEqual(self.proyecto.margen_real_porcentaje, Decimal('88.00'))
