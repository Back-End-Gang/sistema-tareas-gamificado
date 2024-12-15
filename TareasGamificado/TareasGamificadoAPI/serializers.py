from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from tareas.models import Tarea
from usuarios.models import Usuario
from logros.models import Logro

class TareaSerializar(serializers.ModelSerializer):
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

class UserLoginSerializer(serializers.ModelSerializer):
  username = serializers.CharField()
  class Meta:
    model = User
    fields = ['username', 'password']