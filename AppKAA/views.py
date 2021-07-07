from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.urls import reverse
from .forms import ProductoForm, CustomUserCreationForm
from .models import Producto, CategoriaProducto, carrito



# Create your views here. VISTAS

def home(request):
    productos=Producto.objects.all()[0:3]
    secundarios=Producto.objects.all().order_by('-id')[:7]

    data={
        'productos': productos,
        'secundarios': secundarios
    }
    return render (request, 'AppKAA/home.html', data)



def ver_producto(request, id):
    busqueda = request.GET.get("buscar")
    categorias = CategoriaProducto.objects.all()
    prod = get_object_or_404(Producto, id=id)

    if busqueda:
        data = busqueda
        return render(request, 'AppKAA/producto.html', data)
    else:

        data = {
            'producto': prod,
            'categorias': categorias
        }

        return render(request, 'AppKAA/producto.html', data)






def resultado(request):
    if request.method == "POST":
        buscado = request.POST['buscado']
        producto_a=Producto.objects.filter(nombre__icontains=buscado)
        producto_b=Producto.objects.filter(descripcion__icontains=buscado)

        productos = producto_a.union(producto_b)
        return render(request, 'AppKAA/resultado.html', {
            'buscado': buscado,
            'producto': productos
        })
    else:
        return render(request, 'AppKAA/resultado.html', {})





def acerca_de(request):
    return render(request, "AppKAA/acerca_de.html")





def login(request):
    return render(request, "registration/login.html")



def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request)
            messages.success(request, "El usuario ha sido creado correctamente")
            return redirect(to="login")
    return render(request, 'registration/registro.html', data)





@permission_required('AppKAA.add_producto')
def agregar_producto(request):

    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Producto agregado"
        else:
            data["form"] = formulario

    return render(request, 'AppKAA/agregar.html', data)




@permission_required('AppKAA.change_producto')
def modificar_producto(request, id):

    prod = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoForm(instance=prod)
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=prod, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="home")
        else:
            data["form"] = formulario

    return render(request, 'AppKAA/modificar.html', data)




def eliminar_producto(request, id):
    prod = get_object_or_404(Producto, id=id)
    prod.delete()
    return redirect("home")




@login_required
def carts(request):
    cart = carrito.objects.filter(usuario=request.user.id).first()
    categorias = CategoriaProducto.objects.all()
    productos = Producto.objects.all()

    if cart:
        prod_cart = cart.productos.all()       
        data = {
            'cart': cart,
            'cart_prod': prod_cart,
            'productos': productos,
            'categorias': categorias,
            
        }
    else:
        data = {
            'cart': cart,
            'productos': productos,
            'categorias': categorias
        }
    
    return render(request, 'AppKAA/carrito.html', data)



def update_cart(request, id):
    user_cart = carrito.objects.filter(usuario=request.user.id).first()
    productos = Producto.objects.get(id=id)

    if user_cart:
        if not productos in user_cart.productos.all():
            user_cart.productos.add(productos)
        else:
            user_cart.productos.remove(productos)

        new_total = 0

        for item in user_cart.productos.all():
            new_total += item.precio

        user_cart.total = new_total
        user_cart.save()
    else:
        new_cart = carrito()
        new_cart.usuario = request.user
        new_cart.save()
        

        if not productos in new_cart.productos.all():
            new_cart.productos.add(productos)
        else:
            new_cart.productos.remove(productos)

        new_total = 0

        for item in new_cart.productos.all():
            new_total += item.precio

        new_cart.total = new_total
        new_cart.save()
    
    return HttpResponseRedirect(reverse("carrito"))



def clear_cart(request):
    cart = carrito.objects.filter(usuario=request.user.id).first()

    for p in cart.productos.all():
        cart.productos.remove(p)

    cart.total = 0
    cart.save()

    return redirect(to="carrito")


