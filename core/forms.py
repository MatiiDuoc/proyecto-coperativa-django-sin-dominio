from django.forms import ModelForm, Textarea
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from django_recaptcha.fields import ReCaptchaField

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'Descripcion': Textarea(attrs={'rows': 8})
        }
class ArtistaForm(ModelForm):
    #captcha = CaptchaField() #captcha
    captcha = ReCaptchaField() #recaptcha
    class Meta:
        model = Artista
        fields = '__all__'
        widgets = {
            'Descripcion': Textarea(attrs={'rows': 8})
        }
class ForoForm(ModelForm):
    class Meta:
        model = Foro
        fields = '__all__'
        widgets = {
            'Descripcion': Textarea(attrs={'rows': 8})
        }
class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']       

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'