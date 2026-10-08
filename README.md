# Alke Wallet — Proyecto Módulo 7
Descripción creada por mi mejor amigo chatgpt 
Billetera digital de práctica creada con **Python, Django, SQLite, ORM, vistas CRUD, login y CSS rosado pastel**.

**Usuario demo:** `coni`  
**Contraseña demo:** `MichiConPlata2026!`  
**Admin:** http://127.0.0.1:8000/admin/

> Estas credenciales son inventadas y solo sirven para practicar en tu equipo. Nunca publiques una app real con esta clave, `DEBUG=True` ni la `SECRET_KEY` de ejemplo. `cargar_demo` no modifica la contraseña si el usuario ya existe.

## ¿Qué tiene?
- Clientes: listar, crear, editar y eliminar (CRUD con vistas basadas en clases).
- Cuentas: listar y crear billeteras asociadas a clientes.
- Movimientos: depósitos y transferencias con validación de saldo y transacción atómica.
- Reportes: filtros y anotaciones del ORM (`filter`, `annotate`, `Count`).
- Login, logout, CSRF, administración Django, archivos estáticos y pruebas automáticas.

## Archivos principales
- `gestion/models.py`: modelos Cliente, Cuenta, Transaccion.
- `gestion/forms.py`: formularios y validaciones.
- `gestion/views.py`: vistas y consultas ORM.
- `gestion/services.py`: lógica de transferencias segura para la demo.
- `gestion/urls.py`: rutas dinámicas.
- `gestion/tests.py`: pruebas.
- `templates/`: páginas HTML.
- `gestion/static/gestion/css/style.css`: colores y diseño.

```python
from gestion.models import Cliente, Cuenta
from django.db.models import Count
print(list(Cliente.objects.filter(nombre__icontains='coni')))
print(list(Cliente.objects.annotate(total=Count('cuentas')).values('nombre','total')))
print(list(Cuenta.objects.filter(saldo__gt=0).values('alias','saldo')))
# Ejemplo SQL parametrizado:
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('SELECT COUNT(*) FROM gestion_cliente WHERE nombre LIKE %s', ['%Coni%'])
    print(cursor.fetchone())
