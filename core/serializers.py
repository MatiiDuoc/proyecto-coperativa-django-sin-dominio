
from rest_framework import serializers
from .models import *


#lo utilizamos para transformar python a json

#transforma todos los campos de la tabla Producto en json

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'
#transforma todos los campos de la tabla producto  en json
class ProductoSerializer(serializers.ModelSerializer):
    marca = MarcaSerializer(read_only=True)
    class Meta:
        model = Producto
        fields = '__all__'

class ArtistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artista
        fields = '__all__'