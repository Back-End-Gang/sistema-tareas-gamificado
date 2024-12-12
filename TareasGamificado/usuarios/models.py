from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    correo = models.CharField(max_length=255)
    nivel = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nombre