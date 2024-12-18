from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.middleware.csrf import get_token
from TareasGamificadoAPI.serializers import *
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from tareas.models import Tarea
from usuarios.models import Usuario
from logros.models import Logro
from .serializers import TareaSerializer, SerializerCrearToken

# Crea tokens de acceso y refresco para el usuario
def obtener_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class VistaCrearToken(TokenObtainPairView):
    serializer = SerializerCrearToken

@permission_classes([AllowAny]) # Permite entrar a la página sin tener que estar autenticado (versión inversa del decorator @loginrequired)
class VistaLogin(APIView):
    serializer = LoginSerializer

    def get(self, request, format=None):
        # Permite mostrar mensajes de manera dinámica (ej. mostrar mensajes de tokens sólo en la página de la API)
        almacenamiento_mensajes = messages.get_messages(request)
        almacenamiento_mensajes.used = True
        return render(request, "registration/login.html", {'url_actual': request.path})

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            token = obtener_token(user) # Crea la token de acceso
            token_csrf = get_token(request) # Crea la token de CSRF
            response = Response(status=status.HTTP_302_FOUND) and redirect('index_api') # 

            print(f"Token de acceso: {token['access']} \n\n Token de refresco: {token['refresh']} \n\n Token de CSRF: {token_csrf}")

            token_access = str(token['access'])
            token_refresh = str(token['refresh'])

            response.set_cookie(key='access_token', value=token_access, httponly=True)
            response.set_cookie(key='refresh_token', value=token_refresh, httponly=True)
            response.set_cookie(key='csrftoken', value=token_csrf)
            
            print(f"Token de acceso: {token_access} \n\n Token de refresco: {token_refresh} \n\n Token de CSRF: {token_csrf}")

            response.data = {'access_token': token_access, 'refresh_token': token_refresh, 'csrftoken': str(token_csrf)}
            messages.success(request, f"DEV: Inicio de sesión exitoso. Token de acceso: \n{token_access}")
            return response
        else:
            messages.error(request, "Usuario o contraseña inválidos")
            return render(request)

@permission_classes([AllowAny])
@authentication_classes([JWTAuthentication])
class VistaLogout(APIView):

	def get(self, request):
		user_token = request.COOKIES.get('access_token', None) # Busca la cookie con el header del token de acceso del usuario
		if user_token:
			response = Response(status=status.HTTP_302_FOUND) and redirect('index_api')
			response.delete_cookie('access_token') # Elimina el token de acceso creado durante el login
			return response
		response = Response(status=status.HTTP_400_BAD_REQUEST) and redirect('index_api')
		return response

@authentication_classes([JWTAuthentication])
class TareaListar(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogroSerializer

    def get(self, request, format=None):
        ordenar_campo = request.GET.get('ordenar', 'titulo') # Campo por defecto
        ordenar_orden = request.GET.get('orden', 'asc') # Dirección del orden

        if ordenar_orden == 'desc':
            ordenar_campo = f'-{ordenar_campo}'

        tareas = Tarea.objects.all().order_by(ordenar_campo) #Obtiene todos los datos existentes y los ordena según campo

        paginator = Paginator(tareas, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer_class = TareaSerializer(tareas, many=True) # Define el modelo que utilizará
        print(request.path)
        return render(request, 'tareas/ListarTareas.html', {'page_obj': page_obj, 'url_actual': request.path, 'ordenar_campo': request.GET.get('ordenar', ''), 'ordenar_orden': request.GET.get('orden', 'asc')})

@authentication_classes([JWTAuthentication])
class TareaCrear(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    consulta = Tarea.objects.all()
    serializer_class = TareaSerializer

    def get(self, request, *args, **kwargs):
        usuarios = Usuario.objects.all()
        return render(request, 'tareas/CrearTareas.html', {'usuarios': usuarios, 'url_actual': request.path})

    def post(self, request, *args, **kwargs):
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado')
        puntos = request.POST.get('puntos')
        usuario_id = request.POST.get('usuario')
        usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None

        Tarea.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            estado=estado,
            puntos=puntos,
            usuario=usuario,
        )
        return redirect('listar_tareas_api')

@authentication_classes([JWTAuthentication])
class TareaEditar(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TareaSerializer

    def get(self, request, pk, format=None):
        tarea = get_object_or_404(Tarea, id=pk)
        serializer = TareaSerializer(tarea)
        usuarios = Usuario.objects.all()
        return render(request, 'tareas/ActualizarTareas.html', {'tarea': serializer.data, 'usuarios': usuarios})

    def post(self, request, pk, format=None):
        if request.POST.get('_method') == 'PUT':
            tarea = get_object_or_404(Tarea, id=pk)
            serializer = TareaSerializer(tarea, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data) and redirect('listar_tareas_api')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
class TareaEliminar(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TareaSerializer

    def get(self, request, pk, format=None):
        tarea = get_object_or_404(Tarea, id=pk)
        serializer_class = TareaSerializer(tarea)
        return render(request, 'tareas/EliminarTareas.html', {'tarea': serializer_class.data})

    def post(self, request, pk, format=None):
        if request.POST.get('_method') == 'DELETE':
            tarea = get_object_or_404(Tarea, id=pk)
            serializer = TareaSerializer(tarea, data=request.data)
            tarea.delete()
            return redirect('listar_tareas_api')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
class UsuarioListar(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsuarioSerializer

    def get(self, request, format=None):
        usuarios = Usuario.objects.all() #Obtiene todos los datos existentes
        paginator = Paginator(usuarios, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer_class = UsuarioSerializer(usuarios, many=True) # Define el modelo que utilizará
        print(request.path)
        return render(request, 'usuarios/listar_usuarios.html', {'page_obj': page_obj, 'url_actual': request.path})

@authentication_classes([JWTAuthentication])
class UsuarioCrear(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    consulta = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get(self, request, *args, **kwargs):
        usuarios = Usuario.objects.all()
        return render(request, 'usuarios/crear.html', {'usuarios': usuarios, 'url_actual': request.path})

    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        nivel = request.POST.get('nivel')

        # Validate and create the task
        Usuario.objects.create(
            nombre=nombre,
            correo=correo,
            nivel=nivel,
        )
        return redirect('listar_usuarios_api')

@authentication_classes([JWTAuthentication])
class UsuarioEditar(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsuarioSerializer

    def get(self, request, pk, format=None):
        usuario = get_object_or_404(Usuario, id=pk)
        serializer_class = UsuarioSerializer(usuario)
        return render(request, 'usuarios/actualizar_usuario.html', {'usuario': serializer_class.data})

    def post(self, request, pk, format=None):
        if request.POST.get('_method') == 'PUT':
            usuario = get_object_or_404(Usuario, id=pk)
            serializer = UsuarioSerializer(usuario, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data) and redirect('listar_usuarios_api')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
class UsuarioEliminar(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsuarioSerializer

    def get(self, request, pk, format=None):
        usuario = get_object_or_404(Usuario, id=pk)
        serializer = UsuarioSerializer(usuario)
        return render(request, 'usuarios/eliminar_usuario.html', {'usuario': serializer.data})

    def post(self, request, pk, format=None):
        if request.POST.get('_method') == 'DELETE':
            usuario = get_object_or_404(Usuario, id=pk)
            serializer = UsuarioSerializer(usuario, data=request.data)
            usuario.delete()
            return redirect('listar_usuarios_api')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
class LogroListar(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogroSerializer

    def get(self, request, format=None):
        logros = Logro.objects.all() #Obtiene todos los datos existentes
        paginator = Paginator(logros, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serializer = LogroSerializer(logros, many=True) # Define el modelo que utilizará
        print(request.path)
        return render(request, 'logros/listar_logros.html', {'page_obj': page_obj, 'url_actual': request.path})

@authentication_classes([JWTAuthentication])
class LogroCrear(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    consulta = Logro.objects.all()
    serializer = LogroSerializer

    def get(self, request, *args, **kwargs):
        usuarios = Usuario.objects.all()
        return render(request, 'logros/crear.html', {'usuarios': usuarios, 'url_actual': request.path})

    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        usuario_id = request.POST.get('usuario')
        usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None

        # Validate and create the task
        Logro.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            usuario=usuario,
        )
        return redirect('listar_logros_api')

@authentication_classes([JWTAuthentication])
class LogroEditar(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogroSerializer

    def get(self, request, pk, format=None):
        logro = get_object_or_404(Logro, id=pk)
        serializer = LogroSerializer(logro)
        usuarios = Usuario.objects.all()
        return render(request, 'logros/actualizar_logros.html', {'logro': serializer.data, 'usuarios': usuarios})

    def post(self, request, pk, format=None):
        if request.POST.get('_method') == 'PUT':
            logro = get_object_or_404(Logro, id=pk)
            serializer = LogroSerializer(logro, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data) and redirect('listar_logros_api')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
class LogroEliminar(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogroSerializer

    def get(self, request, pk, format=None):
        logro = get_object_or_404(Logro, id=pk)
        serializer = LogroSerializer(logro)
        return render(request, 'logros/eliminar_logros.html', {'logro': serializer.data})

    def post(self, request, pk, format=None):
        if request.POST.get('_method') == 'DELETE':
            logro = get_object_or_404(Logro, id=pk)
            serializer = LogroSerializer(logro, data=request.data)
            logro.delete()
            return redirect('listar_logros_api')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vistas de la base de datos en formato no gráfico tipo JSON
@api_view(['GET', 'POST'])
def tarea_lista(request):
    if request.method == 'GET':
        tarea = Tarea.objects.all()
        serializer = TareaSerializer(tarea, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = TareaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def tarea_detalle(request, pk):
    try:
        tarea = Tarea.objects.get(pk=pk)
    except Tarea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TareaSerializer(tarea)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = TareaSerializer(tarea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        tarea.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def usuario_lista(request):
    if request.method == 'GET':
        usuario = Usuario.objects.all()
        serializer = UsuarioSerializer(usuario, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST', 'DELETE'])
def usuario_detalle(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        usuario.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def logro_lista(request):
    if request.method == 'GET':
        logro = Logro.objects.all()
        serializer = LogroSerializer(logro, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = LogroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST', 'DELETE'])
def logro_detalle(request, pk):
    try:
        logro = Logro.objects.get(pk=pk)
    except Logro.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LogroSerializer(logro)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = LogroSerializer(logro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        logro.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)