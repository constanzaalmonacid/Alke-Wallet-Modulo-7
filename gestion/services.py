from decimal import Decimal
from django.db import transaction
from django.db.models import F
from .models import Cuenta, Transaccion

def registrar_movimiento(*, tipo, origen, destino, monto, detalle=''):
    monto=Decimal(str(monto))
    if monto <= 0:
        raise ValueError('El monto debe ser positivo.')
    with transaction.atomic():
        if tipo=='DEPOSITO':
            Cuenta.objects.filter(pk=destino.pk).update(saldo=F('saldo')+monto)
            origen=None
        elif tipo=='TRANSFERENCIA':
            if origen is None or origen.pk==destino.pk:
                raise ValueError('Selecciona dos cuentas distintas.')
            # Bloqueo transaccional (SQLite serializa escrituras; PostgreSQL soporta select_for_update).
            cuentas={c.pk:c for c in Cuenta.objects.select_for_update().filter(pk__in=[origen.pk,destino.pk]).order_by('pk')}
            if len(cuentas)!=2 or cuentas[origen.pk].saldo < monto:
                raise ValueError('Saldo insuficiente o cuenta no encontrada.')
            Cuenta.objects.filter(pk=origen.pk).update(saldo=F('saldo')-monto)
            Cuenta.objects.filter(pk=destino.pk).update(saldo=F('saldo')+monto)
        else:
            raise ValueError('Tipo de movimiento no válido.')
        return Transaccion.objects.create(tipo=tipo,origen=origen,destino=destino,monto=monto,detalle=detalle)
