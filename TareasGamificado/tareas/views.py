from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Tarea
from usuarios.models import Usuario

# Create your views here.

def Home(request):
    return render(request, 'index.html')

@login_required

def LoginVista(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('home')
        
        else:
            messages.error(request, "Credenciales inválidas")
            return redirect('login')

    return render(request, 'login.html')


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
    return render(request, 'tareas/CrearTareas.html', {'usuarios': usuarios})

@login_required
def listar_tareas(request):
    # Filtrar tareas por el usuario autenticado
    tareas = Tarea.objects.filter(usuario=request.user).select_related('logro')
    paginator = Paginator(tareas, 10)  # 10 tareas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tareas/ListarTareas.html', {'page_obj': page_obj})


@login_required
def actualizar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id, usuario=request.user)  # Verificar que la tarea pertenece al usuario
    if request.method == 'POST':
        tarea.titulo = request.POST.get('titulo')
        tarea.descripcion = request.POST.get('descripcion')
        tarea.save()
        return redirect('listar_tareas')
    return render(request, 'tareas/ActualizarTarea.html', {'tarea': tarea})


@login_required
def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id, usuario=request.user)  # Verificar que la tarea pertenece al usuario
    if request.method == 'POST':
        tarea.delete()
        return redirect('listar_tareas')
    return render(request, 'Tareas/EliminarTarea.html', {'tarea': tarea})