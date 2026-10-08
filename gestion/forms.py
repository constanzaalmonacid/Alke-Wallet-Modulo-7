from django import forms
from .models import Cliente, Cuenta

class ClienteForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=['nombre','email','telefono']

class CuentaForm(forms.ModelForm):
    class Meta:
        model=Cuenta
        fields=['cliente','alias']

class MovimientoForm(forms.Form):
    tipo=forms.ChoiceField(choices=[('DEPOSITO','Depósito'),('TRANSFERENCIA','Transferencia')])
    origen=forms.ModelChoiceField(queryset=Cuenta.objects.none(), required=False, label='Cuenta de origen')
    destino=forms.ModelChoiceField(queryset=Cuenta.objects.none(), label='Cuenta de destino')
    monto=forms.DecimalField(min_value=0.01, max_digits=12, decimal_places=2)
    detalle=forms.CharField(max_length=120, required=False)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['origen'].queryset=Cuenta.objects.select_related('cliente').all()
        self.fields['destino'].queryset=Cuenta.objects.select_related('cliente').all()
    def clean(self):
        datos=super().clean()
        if datos.get('tipo')=='TRANSFERENCIA':
            if not datos.get('origen'):
                self.add_error('origen','Selecciona una cuenta de origen.')
            elif datos.get('origen')==datos.get('destino'):
                self.add_error('destino','Elige una cuenta diferente.')
        return datos
