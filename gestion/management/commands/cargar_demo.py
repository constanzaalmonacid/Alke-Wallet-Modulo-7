from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gestion.models import Cliente,Cuenta,Transaccion
from gestion.services import registrar_movimiento

class Command(BaseCommand):
    help='Carga datos de ejemplo para practicar (solo uso local).'
    def handle(self,*args,**kwargs):
        # Contraseñas ficticias: cambiar antes de publicar cualquier sitio.
        usuario,creado=User.objects.get_or_create(username='coni')
        if creado:
            usuario.set_password('MichiConPlata2026!')
            usuario.is_staff=True
            usuario.is_superuser=True
            usuario.save()
        nombres=[('Coni Almonacid','coni@wallet.test','Coni ahorritos',95000),
                 ('Sofi Villarroel','sofi@wallet.test','Sofi millonaria',42000),
                 ('Luna Estrellita','luna@wallet.test','Fondo de completos',18000)]
        cuentas=[]
        for nombre,email,alias,saldo in nombres:
            cliente,_=Cliente.objects.get_or_create(email=email,defaults={'nombre':nombre})
            if email=='coni@wallet.test' and cliente.usuario_id is None:
                cliente.usuario=usuario;cliente.save(update_fields=['usuario'])
            cuenta,_=Cuenta.objects.get_or_create(cliente=cliente,alias=alias,defaults={'saldo':saldo})
            cuentas.append(cuenta)
        if not Transaccion.objects.exists():
            registrar_movimiento(tipo='TRANSFERENCIA',origen=cuentas[0],destino=cuentas[1],monto=3500,detalle='Por los pancitos 🥐')
            registrar_movimiento(tipo='DEPOSITO',origen=None,destino=cuentas[0],monto=10000,detalle='Premio por sobrevivir a Django')
        self.stdout.write(self.style.SUCCESS('Datos cargados. Usuario: coni / Clave demo: MichiConPlata2026!'))
