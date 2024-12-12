from django.db import models
from usuarios.models import Usuario  # Importa el modelo de usuario extendido


class Tarea(models.Model):
    ESTADOS_CHOICES = [('pendiente', 'Pendiente'), ('completada', 'Completada')]
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES , default='pendiente')
    puntos = models.PositiveIntegerField(default=1)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name="tareas")

    def __str__(self):
        return self.titulo