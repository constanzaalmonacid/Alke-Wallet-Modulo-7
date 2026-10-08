from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Cliente, Cuenta, Transaccion
from .forms import ClienteForm, CuentaForm, MovimientoForm
from .services import registrar_movimiento

@login_required
def inicio(request):
    datos={
      'clientes':Cliente.objects.count(),
      'cuentas':Cuenta.objects.count(),
      'saldo_total':Cuenta.objects.aggregate(total=Sum('saldo'))['total'] or 0,
      'movimientos':Transaccion.objects.select_related('origen','destino').all()[:5],
    }
    return render(request,'gestion/inicio.html',datos)

class ClienteListView(LoginRequiredMixin,ListView):
    model=Cliente
    template_name='gestion/cliente_list.html'
    context_object_name='clientes'

class ClienteCreateView(LoginRequiredMixin,CreateView):
    model=Cliente
    form_class=ClienteForm
    template_name='gestion/form.html'
    success_url=reverse_lazy('cliente_list')
    extra_context={'titulo':'Nuevo cliente'}

class ClienteUpdateView(LoginRequiredMixin,UpdateView):
    model=Cliente
    form_class=ClienteForm
    template_name='gestion/form.html'
    success_url=reverse_lazy('cliente_list')
    extra_context={'titulo':'Editar cliente'}

class ClienteDeleteView(LoginRequiredMixin,DeleteView):
    model=Cliente
    template_name='gestion/confirmar.html'
    success_url=reverse_lazy('cliente_list')

class CuentaListView(LoginRequiredMixin,ListView):
    model=Cuenta
    template_name='gestion/cuenta_list.html'
    context_object_name='cuentas'
    def get_queryset(self):
        return Cuenta.objects.select_related('cliente').all()

class CuentaCreateView(LoginRequiredMixin,CreateView):
    model=Cuenta
    form_class=CuentaForm
    template_name='gestion/form.html'
    success_url=reverse_lazy('cuenta_list')
    extra_context={'titulo':'Nueva billetera'}

@login_required
def movimientos(request):
    if request.method=='POST':
        form=MovimientoForm(request.POST)
        if form.is_valid():
            try:
                registrar_movimiento(**form.cleaned_data)
            except ValueError as error:
                form.add_error(None,str(error))
            else:
                messages.success(request,'¡Movimiento guardado!')
                return redirect('movimientos')
    else:
        form=MovimientoForm()
    historial=Transaccion.objects.select_related('origen','destino')[:30]
    return render(request,'gestion/movimientos.html',{'form':form,'historial':historial})

@login_required
def reporte(request):
    # Consultas ORM personalizadas: filtros, agrupaciones y anotaciones.
    clientes=Cliente.objects.annotate(numero_cuentas=Count('cuentas')).order_by('-numero_cuentas')
    cuentas_con_saldo=Cuenta.objects.filter(saldo__gt=0).select_related('cliente')
    return render(request,'gestion/reporte.html',{'clientes':clientes,'cuentas_con_saldo':cuentas_con_saldo})
