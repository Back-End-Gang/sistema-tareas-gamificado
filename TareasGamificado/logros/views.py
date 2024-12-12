from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Logro

def listar_logros(request):
    logros = Logro.objects.all()
    paginator = Paginator(logros, 10)  # 10 logros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'logros/listar_logros.html', {'page_obj': page_obj})

@login_required
def crear_logro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        usuario = request.user  # Asigna el usuario logueado
        Logro.objects.create(nombre=nombre, descripcion=descripcion, usuario=usuario)
        return redirect('listar_logros')
    return render(request, 'logros/crear_logro.html')

@login_required
def editar_logro(request, id):
    logro = get_object_or_404(Logro, id=id)
    if request.method == 'POST':
        logro.nombre = request.POST.get('nombre')
        logro.descripcion = request.POST.get('descripcion')
        logro.save()
        return redirect('listar_logros')
    return render(request, 'logros/editar_logro.html', {'logro': logro})

@login_required
def eliminar_logro(request, id):
    logro = get_object_or_404(Logro, id=id)
    if request.method == 'POST':
        logro.delete()
        return redirect('listar_logros')
    return render(request, 'logros/eliminar_logro.html', {'logro': logro})
