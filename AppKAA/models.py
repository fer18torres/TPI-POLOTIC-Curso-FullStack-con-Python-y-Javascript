from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CategoriaProducto(models.Model):
    nombre=models.CharField(max_length=65)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="categoriaProd"
        verbose_name_plural="categoriasProd"
    
    def __str__(self):
        return self.nombre


class Producto(models.Model):

    nombre=models.CharField(max_length=100, null=False)
    descripcion=models.CharField(max_length=100, null=False)
    precio=models.FloatField()
    categoria=models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to="productos", blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name="Producto"
        verbose_name_plural="Productos"

    def __str__(self):
        return self.nombre



class carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    productos = models.ManyToManyField(Producto, blank=True)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"Pedido Nro {self.id}"
