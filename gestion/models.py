from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente', null=True, blank=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.nombre

class Cuenta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cuentas')
    alias = models.CharField(max_length=60, default='Mi billetera')
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    def __str__(self):
        return f'{self.alias} - {self.cliente.nombre}'

class Transaccion(models.Model):
    TIPO = [('DEPOSITO','Depósito'),('TRANSFERENCIA','Transferencia')]
    origen = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='enviadas', null=True, blank=True)
    destino = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='recibidas')
    tipo = models.CharField(max_length=20, choices=TIPO)
    monto = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    fecha = models.DateTimeField(auto_now_add=True)
    detalle = models.CharField(max_length=120, blank=True)
    class Meta:
        ordering=['-fecha']
    def __str__(self):
        return f'{self.get_tipo_display()} ${self.monto}'
