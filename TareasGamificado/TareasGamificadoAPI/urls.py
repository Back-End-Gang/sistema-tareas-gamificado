from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from tareas.views import Home


urlpatterns = [
    path('', Home, name='index'),
    path('auth/api-token/', obtain_auth_token, name='auth'),
    path('accounts/login/', UserLoginView.as_view(template_name='registration/login.html'), name='api-login'),
    path('accounts/login/2/', api_login, name='api-login2'),

    path('crear-tareas/', TareaListaCrear.as_view(), name='crear_tarea'),
    path('tareas/<int:pk>/', TareaDetalleEditarEliminar.as_view(), name='listar_tareas'),

    path('crear-usuarios', UsuarioListaCrear.as_view(), name='crear_usuario'),
    path('usuarios/<int:pk>/', UsuarioDetalleEditarEliminar.as_view(), name='listar_usuarios'),
    
    path('crear-logros', LogroListaCrear.as_view(), name='crear_logro'),
    path('logros/<int:pk>/', LogroDetalleEditarEliminar.as_view(), name='listar_logros'),
]
