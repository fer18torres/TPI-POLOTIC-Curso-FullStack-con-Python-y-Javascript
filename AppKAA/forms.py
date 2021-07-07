from AppKAA.models import Producto
from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from models import 



class CrearProducto(forms.ModelForm):
    class Meta:
        model= Producto
        widgets={
            "descripcion": forms.Textarea(attrs={
                "rows":5,
                "cols":30
            })
        }

        fields="__all__"

class ProductoForm(forms.ModelForm):

    class Meta:
        model = models.Producto
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]