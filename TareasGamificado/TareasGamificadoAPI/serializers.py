from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from tareas.models import Tarea
from usuarios.models import Usuario
from logros.models import Logro

# Crea un token para la sesión del usuario
class SerializerCrearToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class LogroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logro
        fields = '__all__'

# Serializer para validar los datos de inicio de sesión
class LoginSerializer(serializers.ModelSerializer):
    # Datos a verificar
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'token']

    def validate(self, attrs):
        return attrs