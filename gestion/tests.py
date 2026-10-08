from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Cliente,Cuenta,Transaccion
from .services import registrar_movimiento

class WalletTests(TestCase):
    def setUp(self):
        self.usuario=User.objects.create_user('test',password='pruebaSegura123!')
        a=Cliente.objects.create(nombre='Coni Almonacid',email='coni@test.cl')
        b=Cliente.objects.create(nombre='Sofi Villarroel',email='sofi@test.cl')
        self.a=Cuenta.objects.create(cliente=a,alias='Coni',saldo=10000)
        self.b=Cuenta.objects.create(cliente=b,alias='Sofi',saldo=0)
    def test_transferencia(self):
        registrar_movimiento(tipo='TRANSFERENCIA',origen=self.a,destino=self.b,monto=3000)
        self.a.refresh_from_db();self.b.refresh_from_db()
        self.assertEqual(self.a.saldo,Decimal('7000'))
        self.assertEqual(self.b.saldo,Decimal('3000'))
        self.assertEqual(Transaccion.objects.count(),1)
    def test_saldo_insuficiente(self):
        with self.assertRaises(ValueError):
            registrar_movimiento(tipo='TRANSFERENCIA',origen=self.a,destino=self.b,monto=20000)
        self.assertEqual(Transaccion.objects.count(),0)
    def test_deposito(self):
        registrar_movimiento(tipo='DEPOSITO',origen=None,destino=self.b,monto=500)
        self.b.refresh_from_db()
        self.assertEqual(self.b.saldo,Decimal('500'))
    def test_login_obligatorio(self):
        self.assertEqual(self.client.get(reverse('cliente_list')).status_code,302)
        self.client.login(username='test',password='pruebaSegura123!')
        self.assertEqual(self.client.get(reverse('cliente_list')).status_code,200)
    def test_crear_cliente(self):
        self.client.force_login(self.usuario)
        response=self.client.post(reverse('cliente_nuevo'),{'nombre':'Luna','email':'luna@test.cl','telefono':''})
        self.assertEqual(response.status_code,302)
        self.assertTrue(Cliente.objects.filter(email='luna@test.cl').exists())
