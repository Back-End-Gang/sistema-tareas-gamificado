from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import *
from tareas.views import Home, logoutVista
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', Home, name='index_api'),
    path('accounts/login/', VistaLogin.as_view(), name='api-login'),
    path('accounts/logout/', VistaLogout.as_view(), name='api-logout'),
    path('token/', VistaCrearToken.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('crear_tarea/', TareaCrear.as_view(), name='crear_tarea_api'),
    path('listar_tareas/', TareaListar.as_view(), name='listar_tareas_api'),
    path('actualizar_tarea/<int:pk>/', TareaEditar.as_view(), name='actualizar_tarea_api'),
    path('eliminar_tarea/<int:pk>/', TareaEliminar.as_view(), name='eliminar_tarea_api'),

    path('crear_usuario/', UsuarioCrear.as_view(), name='crear_usuario_api'),
    path('listar_usuarios/', UsuarioListar.as_view(), name='listar_usuarios_api'),
    path('actualizar_usuario/<int:pk>/', UsuarioEditar.as_view(), name='actualizar_usuario_api'),
    path('eliminar_usuario/<int:pk>/', UsuarioEliminar.as_view(), name='eliminar_usuario_api'),
    
    path('crear_logro/', LogroCrear.as_view(), name='crear_logro_api'),
    path('listar_logros/', LogroListar.as_view(), name='listar_logros_api'),
    path('actualizar_logros/<int:pk>/', LogroEditar.as_view(), name='actualizar_logro_api'),
    path('eliminar_logros/<int:pk>/', LogroEliminar.as_view(), name='eliminar_logro_api'),
]