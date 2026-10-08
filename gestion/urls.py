from django.urls import path
from . import views
urlpatterns=[
 path('',views.inicio,name='inicio'),
 path('clientes/',views.ClienteListView.as_view(),name='cliente_list'),
 path('clientes/nuevo/',views.ClienteCreateView.as_view(),name='cliente_nuevo'),
 path('clientes/<int:pk>/editar/',views.ClienteUpdateView.as_view(),name='cliente_editar'),
 path('clientes/<int:pk>/eliminar/',views.ClienteDeleteView.as_view(),name='cliente_eliminar'),
 path('cuentas/',views.CuentaListView.as_view(),name='cuenta_list'),
 path('cuentas/nueva/',views.CuentaCreateView.as_view(),name='cuenta_nueva'),
 path('movimientos/',views.movimientos,name='movimientos'),
 path('reportes/',views.reporte,name='reporte'),
]
