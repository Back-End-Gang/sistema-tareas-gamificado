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
from logros.views import *
from TareasGamificadoAPI import views as tarea_views
from LogrosGamificadoAPI import views as logro_views
from UsuariosGamificadoAPI import views as usuario_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='index'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html')),
    #tarea
    path('crear_tarea/', crear_tarea, name='crear_tarea'),
    path('listar_tareas/', listar_tareas, name='listar_tareas'),
    path('actualizar_tarea/<int:id>/', actualizar_tarea, name='actualizar_tarea'),
    path('eliminar_tarea/<int:id>/', eliminar_tarea, name='eliminar_tarea'),
    #usuarios
    path('listar_usuarios/', listar_usuarios, name='listar_usuarios'),
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    path('editar_usuario/<int:id>/', editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:id>/', eliminar_usuario, name='eliminar_usuario'),
    #logros
    path('listar_logros/', listar_logros, name='listar_logros'),
    path('crear/', crear_logro, name='crear_logro'),
    path('actualizar_logros/<int:id>/', editar_logro, name='editar_logro'),
    path('eliminar_logro/<int:id>/', eliminar_logro, name='eliminar_logro'),
    #API Tarea
    path('tareasListApi/', tarea_views.tarea_list, name='tareaListaAPI'),
    path('tareasListApi/<int:pk>/', tarea_views.tarea_detail, name='tarea_detail'),
    #API Logro
    path('logrosListApi/', logro_views.logros_list, name='logrosListaAPI'),
    path('logrosListApi/<int:pk>/', logro_views.logros_detail, name='logros_detail'),
    #API Usuario
    path('usuariosListApi/', usuario_views.usuarios_list, name='usuariosListaAPI'),
    path('usuariosListApi/<int:pk>/', usuario_views.usuarios_detail, name='usuarios_detail'),
    
]