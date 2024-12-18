from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .models import Tarea
from usuarios.models import Usuario
from TareasGamificado.decorators.excluir_jwt import excluido_jwt

# Create your views here.

@permission_classes([AllowAny])
@excluido_jwt
def Home(request):
    return render(request, 'index.html', {'url_actual': request.path})

@login_required
def logoutVista(request):
    logout(request)
    print(request.path)
    return render(request, 'registration/logout.html', {'logout_url_actual': request.path})

@excluido_jwt
def LoginVista(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('crear')
        
        else:
            messages.error(request, "Credenciales inválidas")
            return redirect('login')

    return render(request, 'login.html', {'url_actual': request.path})

@excluido_jwt
@login_required
def crear_tarea(request):
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado')
        puntos = request.POST.get('puntos')
        usuario_id = request.POST.get('usuario')
        usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None

        # Asociar la tarea con el usuario autenticado
        Tarea.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            estado=estado,
            puntos=puntos,
            usuario=usuario,
        )
        return redirect('listar_tareas')
    return render(request, 'tareas/CrearTareas.html', {'usuarios': usuarios, 'url_actual': request.path})

@login_required
@excluido_jwt
def listar_tareas(request):
    tareas = Tarea.objects.select_related('usuario').all()
    paginator = Paginator(tareas, 10)  # 10 tareas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tareas/ListarTareas.html', {'page_obj': page_obj})


@login_required
@excluido_jwt
def actualizar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        tarea.titulo = request.POST.get('titulo')
        tarea.descripcion = request.POST.get('descripcion')
        usuario_id = request.POST.get('usuario')
        tarea.estado = request.POST.get('estado')
        tarea.puntos = request.POST.get('puntos')
        tarea.usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None
        
        tarea.save()
        return redirect('listar_tareas')
    return render(request, 'tareas/ActualizarTareas.html', {'tarea': tarea, 'usuarios': usuarios})


@login_required
@excluido_jwt
def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    if request.method == 'POST':
        tarea.delete()
        return redirect('listar_tareas')
    return render(request, 'Tareas/EliminarTareas.html', {'tarea': tarea})