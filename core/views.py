import json
from pipes import quote
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from rest_framework import viewsets
from .serializers import *
from rest_framework.renderers import JSONRenderer
import requests
from django.contrib.auth import login
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from reportlab.pdfgen import canvas
from django.core import serializers as core_serializers
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.db.models import Func



class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 0)'  # Cambia el 2 por el número de decimales que desees

#utilizamos los viewsets para manejar las solicitudes http (get, post, put, delete)
class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all().order_by('id')
    serializer_class = MarcaSerializer
    renderer_classes = [JSONRenderer]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('id')
    serializer_class = ProductoSerializer
    renderer_classes = [JSONRenderer]
    
class ArtistaViewSet(viewsets.ModelViewSet):
    queryset = Artista.objects.all().order_by('id')
    serializer_class = ArtistaSerializer
    renderer_classes = [JSONRenderer]
# Create your views here.

def index(request):
    return render(request, 'core/pages/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #autentificar
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Usuario o contraseña incorrectos')
            return render(request, 'core/pages/login.html')
    return render(request, 'core/pages/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def foro(request):
    foros = Foro.objects.all()
    aux = {
        'lista': foros
    }

    return render(request, 'core/pages/foro.html', aux)

def artista(request):
    artistas = Artista.objects.all()
    aux = {
        'lista': artistas
    }

    return render(request, 'core/pages/artistas.html', aux)

def producto(request):
    productos = Producto.objects.all()
    aux = {
        'lista': productos
    }

    return render(request, 'core/pages/productos.html', aux)

def contacto(request):
    return render(request, 'core/pages/contacto.html')

def registro(request):
    aux = {
        'form': RegistroForm()
    }

    if request.method == 'POST':
        formulario = RegistroForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            #asignamor un grupo al usuario creado
            grupo = Group.objects.get(name='Cliente')
            user.groups.add(grupo)
            #Mensaje
            messages.success(request, 'Usuario registrado correctamente!')
            #autentifica y loguea
            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            login(request, user)
            return redirect('index')
        else:
            aux['form'] = formulario

    return render(request, 'core/pages/registro.html', aux)

@login_required
def agregar_foro(request):
    aux = {
        'form': ForoForm()
    }

    if request.method == 'POST':
        form = ForoForm(data=request.POST)
        if form.is_valid():
            form.save()
            aux['form'] = form
            messages.success(request, 'Post agregado correctamente!')
        else:
            aux['form'] = form
            messages.error(request, 'El post no se pudo agregar')

    return render(request, 'core/pages/agregar_foro.html',aux)

def detalle_producto(request, id):
    producto = Producto.objects.get(id=id)
    
    aux = {
        'producto' : producto
    }
    return render (request, 'core/pages/detalle_producto.html', aux)

def detalle_artista(request, id):
    artista = Artista.objects.get(id=id)
    
    aux = {
        'artista' : artista
    }
    return render (request, 'core/pages/detalle_artista.html', aux)

#buscar producto
def buscar_producto(request):
    query = request.GET.get('q')
    productos = []  # Inicializa la lista de productos vacía

    if query:
        # Codifica el query para manejar caracteres especiales
        encoded_query = quote(query)
        # Asume que la API soporta la búsqueda por el parámetro 'q'
        response = requests.get(f'http://127.0.0.1:8000/apiproductos/?q={encoded_query}')
        productos = response.json()

        # Verifica si la API devuelve una estructura que necesita ser paginada directamente
        if isinstance(productos, dict) and 'results' in productos:
            productos = productos['results']
    else:
        # Si no hay query, podrías decidir no mostrar ningún producto o mostrar todos
        # En este ejemplo, elegimos no mostrar ningún producto
        productos = []

    paginator = Paginator(productos, 4)  # Ajusta el número según tus necesidades
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    aux = {
        'page_obj': page_obj
    }

    return render(request, 'core/pages/crudAPI/index.html', aux)

#API
#Si queremos consumir una API externa, es lo mismo que estaba aca abajo, si queremos consumir 2 a la vez se debe de generar otro response y otro aux
#también los productos y lo pasamos a la variable aux
def productosapi(request):
    #productos = Producto.objects.all()
    response = requests.get('http://127.0.0.1:8000/apiproductos/')
    #lo pasa a formato legible
    productos = response.json()
    #paginacion
    paginator = Paginator(productos, 4) #muestra 2 datos por pagina
    page_number = request.GET.get('page')#obtiene el numero de la pagina
    page_obj = paginator.get_page(page_number)#obtiene el objeto de la pagina
    aux = {
        'page_obj': page_obj
    }

    return render(request, 'core/pages/crudAPI/index.html', aux)

# Dashboard
@permission_required('core.view_dashboard')
def dashboard(request):
    productos = Producto.objects.all()
    usuarios = User.objects.all()
    artistas = Artista.objects.all()
    ventas = HistorialCompra.objects.all().aggregate(models.Sum('total'))['total__sum'] or 0
    ventas_por_mes = HistorialCompra.objects.annotate(mes=TruncMonth('fecha')).values('mes').annotate(total=Round(Sum('total'))).order_by('mes')
    aux = {
        'segment': 'index',
        'productos': productos,
        'usuarios': usuarios,
        'artistas': artistas,
        'ventas_totales': ventas,
        'ventas_por_mes': ventas_por_mes,
    }

    return render(request, 'core/pages/dashboard/index.html', aux)

# Usuarios
@permission_required('core.view_user')
def dashboardUsuarios(request):
    usuarios = User.objects.all().order_by('id')
    aux = {
        'segment': 'usuarios',
        'usuarios': usuarios,
    }

    return render(request, 'core/pages/dashboard/usuarios/index.html', aux)

@permission_required('core.add_user')
def agregar_usuario(request):
    aux = {
        'segment': 'usuarios',
        'form': UserForm(),
    }

    if request.method == 'POST':
        form = UserForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            aux['form'] = form
            messages.success(request, 'Usuario agregado correctamente!')
            return redirect('dashboard-usuarios')
        else:
            aux['form'] = form
            messages.error(request, 'El usuario no se pudo agregar')

    return render(request, 'core/pages/dashboard/usuarios/agregar.html', aux)

@permission_required('core.change_user')
def actualizar_usuario(request, id):
    user = User.objects.get(id=id)
    aux = {
        'segment': 'usuarios',
        'form': UserForm(instance=user)
    }
    
    if request.method == 'POST':
        form = UserForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            aux['form'] = form
            messages.success(request, 'Usuario actualizado correctamente!')
        else:
            aux['form'] = form
            messages.error(request, 'El usuario no se pudo actualizar')
    
    return render(request, 'core/pages/dashboard/usuarios/actualizar.html', aux)

@permission_required('core.delete_user')
def eliminar_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()   
    return redirect('dashboard-usuarios')

# Productos
@permission_required('core.view_producto')
def dashboardProductos(request):
    productos = Producto.objects.all().order_by('id')
    aux = {
        'segment': 'productos',
        'productos': productos,
    }

    return render(request, 'core/pages/dashboard/productos/index.html', aux)

@permission_required('core.add_producto')
def agregar_producto(request):
    productos = Producto.objects.all()
    aux = {
        'segment': 'productos',
        'form': ProductoForm(),
    }

    if request.method == 'POST':
        form = ProductoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            aux['form'] = form
            messages.success(request, 'Producto agregado correctamente!')
            return redirect('dashboard-productos')
        else:
            aux['form'] = form
            messages.error(request, 'El producto no se pudo agregar')

    return render(request, 'core/pages/dashboard/productos/agregar.html', aux)

@permission_required('core.change_producto')
def actualizar_producto(request, id):
    producto = Producto.objects.get(id=id)
    aux = {
        'segment': 'productos',
        'form': ProductoForm(instance=producto)
    }
    
    if request.method == 'POST':
        form = ProductoForm(data=request.POST, instance=producto)
        if form.is_valid():
            form.save()
            aux['form'] = form
            messages.success(request, 'Producto actualizado correctamente!')
        else:
            aux['form'] = form
            messages.error(request, 'El producto no se pudo actualizar')
    
    return render(request, 'core/pages/dashboard/productos/actualizar.html', aux)

@permission_required('core.delete_producto')
def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('dashboard-productos')

# Artistas
@permission_required('core.view_artista')
def dashboardArtistas(request):
    artistas = Artista.objects.all().order_by('id')
    aux = {
        'segment': 'artistas',
        'artistas': artistas,
    }

    return render(request, 'core/pages/dashboard/artistas/index.html', aux)


@permission_required('core.add_artista')
def agregar_artista(request):
    aux = {
        'segment': 'artistas',
        'form': ArtistaForm()
    }

    if request.method == 'POST':
        form = ArtistaForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            aux['form'] = form
            messages.success(request, 'Artista agregado correctamente!')
            return redirect('dashboard-artistas')
        else:
            aux['form'] = form
            messages.error(request, 'El artista no se pudo agregar')

    return render(request, 'core/pages/dashboard/artistas/agregar.html',aux)

@permission_required('core.change_artista')
def actualizar_artista(request, id):
    artista = Artista.objects.get(id=id)
    aux = {
        'segment': 'artistas',
        'form': ArtistaForm(instance=artista)
    }
    
    if request.method == 'POST':
        form = ArtistaForm(data=request.POST, instance=artista)
        if form.is_valid():
            form.save()
            aux['form'] = form
            messages.success(request, 'Artista actualizado correctamente!')
        else:
            aux['form'] = form
            messages.error(request, 'El artista no se pudo actualizar')
    
    return render(request, 'core/pages/dashboard/artistas/actualizar.html', aux)

@permission_required('core.delete_artista')
def eliminar_artista(request, id):
    artista = Artista.objects.get(id=id)
    artista.delete()
    return redirect('dashboard-artistas')

def account_locked(request):
    return render(request, 'core/pages/account_locked.html')



@login_required
def add_to_cart(request, producto_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    producto = get_object_or_404(Producto, id=producto_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, producto=producto)
    
    if not created:
        cart_item.cantidad += 1
    else:
        cart_item.cantidad = 1
    
    if producto.Cantidad >= cart_item.cantidad:
        cart_item.save()
        return redirect('ver_carrito')  # Redirige al usuario a la vista del carrito
    else:
        return JsonResponse({'error': 'No hay suficiente cantidad disponible'}, status=400)

#compra con exito
def compra_exitosa(request):
    # Lógica para procesar la compra aquí
    # Obtener el carrito del usuario y limpiarlo
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=request.user.cart)

    historial = HistorialCompra.objects.create(usuario=request.user, total=sum(item.producto.Precio * item.cantidad for item in cart_items))

    HistorialCompraItem.objects.bulk_create([
        HistorialCompraItem(historial=historial, producto=item.producto, cantidad=item.cantidad, precio=item.producto.Precio)
        for item in cart_items
    ])

    for item in cart_items:
        item.producto.Cantidad -= item.cantidad
        item.producto.save()

    cart.clear_cart()

    return redirect('historial_compras')
@login_required
def ver_carrito(request):
    #cart, _ = Cart.objects.get_or_create(user=request.user)
    #cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=request.user.cart)
    total = sum(item.producto.Precio * item.cantidad for item in cart_items)
    #cart.clear_cart()
    return render(request, 'core/pages/ver_carrito.html', {'cart_items': cart_items, 'total': total})

#historial de compras
def historial_compras(request):
    historial_compras = HistorialCompra.objects.filter(usuario=request.user)
    aux = {
        'historial_compras': historial_compras
    }
    return render(request, 'core/pages/historial_compras.html', aux)

@require_POST
def modificar_cantidad_producto(request, producto_id):
    data = json.loads(request.body)
    accion = data.get('accion')
    producto = get_object_or_404(Producto, id=producto_id)
    cart_item, created = CartItem.objects.get_or_create(cart=request.user.cart, producto=producto)
    producto_eliminado = False

    if accion == 'agregar':
        cart_item.cantidad += 1
    elif accion == 'restar':
        cart_item.cantidad -= 1
        if cart_item.cantidad <= 0:
            cart_item.delete()
            producto_eliminado = True
            return JsonResponse({'message': 'Producto eliminado del carrito'})
    cart_item.save()
    return JsonResponse({'message': 'Cantidad actualizada'})

#def procesar_compra(request):
    # Lógica para procesar la compra aquí

    # Obtener el carrito del usuario y limpiarlo
    #cart = Cart.objects.get(user=request.user)
    #cart.clear_cart()

    # Redirigir al usuario o enviar una respuesta
    #return redirect('productos')

#descargar pdf

def descargar_comprobante(request):
    # Crear una respuesta HTTP de tipo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="comprobante_compra.pdf"'

    # Crear un objeto PDF
    p = canvas.Canvas(response)

    # Aquí puedes agregar el contenido del PDF, como texto e imágenes
    p.drawString(100, 100, "Comprobante de Compra")

    # Finalizar el PDF
    p.showPage()
    p.save()

    return response