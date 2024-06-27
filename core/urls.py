from operator import index
from django.contrib import admin
from django.urls import include, path
from .views import * # Importamos todas las vistas de core/views.py 
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from core import views

#configuracion para el admin
#endpoint --> informacion de lo que me esta indicanado
router = routers.DefaultRouter()
router.register('productos', ProductoViewSet)
router.register('marcas', MarcaViewSet)
router.register('artistas', ArtistaViewSet)

urlpatterns = [
    path('login', login_view, name='login'),
    path('registro', registro, name='registro'),
    path('logout', logout_view, name='logout'),
    path('', index, name='index'),
    path('productos', producto, name='productos'),
    path('producto/<id>', detalle_producto, name='detalle_producto'),
    path('artistas', artista, name='artistas'),
    path('artista/<id>', detalle_artista, name='detalle_artista'),
    path('foro', foro, name='foro'),
    path('foro/agregar/', agregar_foro, name='agregar_foro'),
    path('contacto', contacto, name='contacto'),
    path('buscar_producto/', buscar_producto, name='buscar_producto'),

    #API
    path('api', include(router.urls)),
    path('productosapi', productosapi, name='productosapi'),

    # Dashboard
    path('dashboard', dashboard, name='dashboard'),
    # Usuarios
    path('dashboard/usuarios', dashboardUsuarios, name='dashboard-usuarios'),
    path('dashboard/usuarios/agregar', agregar_usuario, name='agregar_usuario'),
    path('dashboard/usuarios/actualizar/<id>', actualizar_usuario, name='actualizar_usuario'),
    path('dashboard/usuarios/eliminar/<id>', eliminar_usuario, name='eliminar_usuario'),
    # Productos
    path('dashboard/productos', dashboardProductos, name='dashboard-productos'),
    path('dashboard/productos/agregar', agregar_producto, name='agregar_producto'),
    path('dashboard/productos/actualizar/<id>', actualizar_producto, name='actualizar_producto'),
    path('dashboard/productos/eliminar/<id>', eliminar_producto, name='eliminar_producto'),
    # Artistas
    path('dashboard/artistas', dashboardArtistas, name='dashboard-artistas'),
    path('dashboard/artistas/agregar', agregar_artista, name='agregar_artista'),
    path('dashboard/artistas/actualizar/<id>', actualizar_artista, name='actualizar_artista'),
    path('dashboard/artistas/eliminar/<id>', eliminar_artista, name='eliminar_artista'),
    #cuenta bloqueada
    path('account_locked/', account_locked, name='account_locked'),
    #carrito
    path('add_to_cart/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('modificar_cantidad_producto/<int:producto_id>/', modificar_cantidad_producto, name='modificar_cantidad_producto'),
    #historial de compras
    path('historial_compras/', views.historial_compras, name='historial_compras'),
    #compra con exito
    path('compra_exitosa/', views.compra_exitosa, name='compra_exitosa'),
    #descargar comprobante
    path('descargar_comprobante/', views.descargar_comprobante, name='descargar_comprobante'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
