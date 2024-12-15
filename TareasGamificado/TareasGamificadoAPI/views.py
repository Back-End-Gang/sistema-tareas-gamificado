from tareas.models import Tarea
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from TareasGamificadoAPI.serializers import *
from rest_framework.response import Response
from rest_framework import status, authentication, generics, exceptions
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect, render
from usuarios.models import Usuario
from logros.models import Logro

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    print("token regenerado")
    return print(refresh.access_token), {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def api_login(request):
    authentication_classes = [TokenAuthentication]

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    if user:
        print('okay!!!! :3')
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK), redirect('index')
    else:
        print('invalido')
        return Response({
            "error": "Usuario o contraseña inválidos"
        }, status=status.HTTP_401_UNAUTHORIZED), redirect('login')

@api_view(['POST'])
def api_vista_login(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])

    if user:
        print('okay!!!! :3')
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        print('invalido')
        return Response({
            "error": "Usuario o contraseña inválidos"
        }, status=status.HTTP_401_UNAUTHORIZED), redirect('login')
    
class UserLoginView(APIView):
    permission_classes = [AllowAny] 

    template_name = "registration/login.html"

    def get(self, request, format=None):
        return render(request, self.template_name)

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK) and redirect('index')
        else:
            print('error')
            return Response({'errors':{'non_field_errors':['Username or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class TareaListaCrear(generics.ListCreateAPIView):
    queryset = Tarea.objects.all() #Obtiene todos los datos existentes
    serializer_class = TareaSerializar # Define el modelo que utilizará

class TareaDetalleEditarEliminar(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializar


class UsuarioListaCrear(generics.ListCreateAPIView):
    queryset = Usuario.objects.all() #Obtiene todos los datos existentes
    serializer_class = UsuarioSerializer # Define el modelo que utilizará

class UsuarioDetalleEditarEliminar(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class LogroListaCrear(generics.ListCreateAPIView):
    queryset = Logro.objects.all() #Obtiene todos los datos existentes
    serializer_class = LogroSerializer # Define el modelo que utilizará

class LogroDetalleEditarEliminar(generics.RetrieveUpdateDestroyAPIView):
    queryset = Logro.objects.all()
    serializer_class = LogroSerializer
