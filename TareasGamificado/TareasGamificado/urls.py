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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from tareas.views import *
from usuarios.views import *
from logros.views import *
from TareasGamificadoAPI import views as tarea_views
from TareasGamificadoAPI import urls as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='index'),
    path('api/', include(api_urls)),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', logoutVista, name='logout'),
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
]