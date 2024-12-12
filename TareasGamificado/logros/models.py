from django.db import models
from usuarios.models import Usuario  # Importa el modelo de usuario extendido

class Logro(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,  # Permitir valores nulos
        related_name="logros"  # Relación reverse
    )

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username if self.usuario else 'Sin usuario'}"
