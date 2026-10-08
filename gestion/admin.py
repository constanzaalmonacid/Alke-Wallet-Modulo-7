from django.contrib import admin
from .models import Cliente,Cuenta,Transaccion
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display=('nombre','email','telefono')
    search_fields=('nombre','email')
@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display=('alias','cliente','saldo')
    list_filter=('cliente',)
@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display=('tipo','origen','destino','monto','fecha')
    list_filter=('tipo',)
    def has_add_permission(self,request):
        return False # Los saldos solo se modifican mediante el servicio transaccional.
    def has_change_permission(self,request,obj=None):
        return False
    def has_delete_permission(self,request,obj=None):
        return False
