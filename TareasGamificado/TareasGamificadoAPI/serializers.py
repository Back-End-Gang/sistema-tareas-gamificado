from rest_framework import serializers
from tareas.models import Tarea

class TareaSerializar(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'