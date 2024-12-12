"""TareasGamificado URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from tareas.views import crear_tarea, listar_tareas, actualizar_tarea, eliminar_tarea, Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='index'),
    path('crear/', crear_tarea, name='CrearTareas'),
    path('listar/', listar_tareas, name='ListarTareas'),
    path('actualizar/<int:id>/', actualizar_tarea, name='ActualizarTareas'),
    path('eliminar/<int:id>/', eliminar_tarea, name='EliminarTareas'),
]