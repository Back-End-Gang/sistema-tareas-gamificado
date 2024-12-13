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
from django.contrib.auth import views as auth_views
from django.contrib import admin
from tareas.views import crear_tarea, listar_tareas, actualizar_tarea, eliminar_tarea, Home, LoginVista
from usuarios.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='index'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html')),
    path('crear_tarea/', crear_tarea, name='crear_tarea'),
    path('listar_tareas/', listar_tareas, name='listar_tareas'),
    path('actualizar_tarea/<int:id>/', actualizar_tarea, name='actualizar_tarea'),
    path('eliminar_tarea/<int:id>/', eliminar_tarea, name='eliminar_tarea'),
    path('listar_usuarios', listar_usuarios, name='listar_usuarios'),
    path('crear_usuario', crear_usuario, name='listar_usuarios'),
    path('editar_usuario', editar_usuario, name='listar_usuarios'),
    path('eliminar_usuario', eliminar_usuario, name='listar_usuarios')
]