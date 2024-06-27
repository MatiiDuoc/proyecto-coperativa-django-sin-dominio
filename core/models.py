from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#Marca
class Marca(models.Model):
    Nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.Nombre
#Producto
class Producto(models.Model):
    Nombre = models.CharField(max_length=50)
    Marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    Cantidad = models.FloatField(default=0)
    Precio = models.FloatField(default=0)
    Descripcion = models.CharField(max_length=1000)
    Imagen = models.ImageField(upload_to='productos', null=True, blank=True)

    def __str__(self):
        return self.Nombre
#Artista
class Artista(models.Model):
    Nombre = models.CharField(max_length=50)
    Descripcion = models.CharField(max_length=1000)
    Imagen = models.ImageField(upload_to='artistas', null=True, blank=True)

    def __str__(self):
        return self.Nombre
#Foro
class Foro(models.Model):
    Nombre = models.CharField(max_length=50)
    Descripcion = models.CharField(max_length=1000)

    def __str__(self):
        return self.Nombre
    
#carrito de compras
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def clear_cart(self):
        self.items.all().delete()  # Asumiendo que `items` es la relación inversa desde CartItem a Cart

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

#historial de compras
class HistorialCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)


class HistorialCompraItem(models.Model):
    historial = models.ForeignKey(HistorialCompra, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)


#ventas para mostrar en el dashboard
class Venta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Opcional: Calcular el subtotal aquí si decides almacenarlo
        super().save(*args, **kwargs)

#compras
class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    # Puedes agregar más campos según necesites

    def __str__(self):
        return f"Compra {self.id} - {self.usuario.username}"