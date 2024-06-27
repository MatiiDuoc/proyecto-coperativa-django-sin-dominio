from django.contrib import admin
from .models import *
from django.contrib.admin import ModelAdmin
from admin_confirm import AdminConfirmMixin

class ProductoModelAdmin(AdminConfirmMixin, ModelAdmin):
        confirm_change = True
        confirmation_fields = ['titulo', 'descripcion']
# Register your models here.
admin.site.register(Marca)
admin.site.register(Producto, ProductoModelAdmin)
admin.site.register(Artista)
admin.site.register(Foro)