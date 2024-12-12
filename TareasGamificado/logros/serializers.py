from rest_framework import serializers
from .models import Logro
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer

class LogroSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer
    usuario_id = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all(), source='usuario', write_only=True)

    class Meta:
        model = Logro
        fields = ['id', 'usuario', 'usuario_id', 'nombre_de_logro', 'descripcion']