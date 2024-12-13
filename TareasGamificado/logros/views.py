from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Logro
from usuarios.models import Usuario

def listar_logros(request):
    logros = Logro.objects.all()
    paginator = Paginator(logros, 10)  # 10 logros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'logros/listar_logros.html', {'page_obj': page_obj})

@login_required
def crear_logro(request):
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        usuario_id = request.POST.get('usuario')
        usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None
        Logro.objects.create(nombre=nombre, descripcion=descripcion, usuario=usuario)
        return redirect('listar_logros')
    return render(request, 'logros/crear.html', {'usuarios': usuarios})

@login_required
def editar_logro(request, id):
    logro = get_object_or_404(Logro, id=id)
    if request.method == 'POST':
        logro.nombre = request.POST.get('nombre')
        logro.descripcion = request.POST.get('descripcion')
        logro.usuario = request.POST.get('usuario')
        logro.save()
        return redirect('listar_logros')
    return render(request, 'logros/actualizar_logros.html', {'logro': logro})

@login_required
def eliminar_logro(request, id):
    logro = get_object_or_404(Logro, id=id)
    if request.method == 'POST':
        logro.delete()
        return redirect('listar_logros')
    return render(request, 'logros/eliminar_logros.html', {'logro': logro})
