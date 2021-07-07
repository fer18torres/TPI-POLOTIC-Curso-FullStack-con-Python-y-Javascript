from django.contrib import admin
from .models import CategoriaProducto, Producto, carrito



class CategoriaProdAdmin(admin.ModelAdmin):
    readonly_fields=("created", "updated")


class ProductoAdmin(admin.ModelAdmin):
    readonly_fields=("created", "updated")

admin.site.register(CategoriaProducto, CategoriaProdAdmin)

admin.site.register(Producto, ProductoAdmin)

admin.site.register(carrito)