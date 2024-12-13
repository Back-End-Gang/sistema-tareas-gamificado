from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Usuario

@login_required
def listar_usuarios(request):
    usuarios = Usuario.objects.all() # Selecciona todos los objetos de la clase
    paginator = Paginator(usuarios, 5)  # Cantidad de entradas a mostrar por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'usuarios/listar_usuarios.html', {'page_obj': page_obj})

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        nivel = request.POST.get('nivel')
        Usuario.objects.create(nombre=nombre, correo=correo, nivel=nivel)
        return redirect('listar_usuarios')
    return render(request, 'usuarios/crear.html')

@login_required
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre')
        usuario.correo = request.POST.get('correo')
        usuario.nivel = request.POST.get('nivel')
        usuario.save()
        return redirect('listar_usuarios')
    return render(request, 'usuarios/actualizar_usuario.html', {'usuario': usuario})

@login_required
def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})