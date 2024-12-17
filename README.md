# sistema-tareas-gamificado


# 1. Logro
El modelo Logro representa un logro que se asocia a un usuario dentro de la aplicación. Puede ser utilizado para registrar cualquier tipo de éxito, tarea completada o meta alcanzada por un usuario.

# Campos:
# nombre(CharField):
Tipo: CharField
Descripción: El nombre o título del logro. Este campo almacena una breve descripción del logro, como por ejemplo: "Usuario del mes", "Nivel completado", etc.
Longitud máxima: 100 caracteres.

# descripcion (TextField):
Tipo: TextField
Descripción: Un campo de texto donde se describe en detalle el logro. Este campo puede contener información más detallada sobre el logro, por ejemplo cómo se alcanzó, los pasos seguidos o el impacto del logro.

# usuario (ForeignKey):
Tipo: ForeignKey
Descripción: Este campo establece una relación con el modelo Usuario, lo que significa que cada logro está vinculado a un usuario específico.
Comportamiento en caso de eliminación: Cuando un usuario es eliminado, este campo se establece en NULL (on_delete=models.SET_NULL), lo que garantiza que los logros no sean eliminados junto con el usuario.
null=True: Permite que este campo pueda ser nulo, es decir, un logro puede no estar asociado a ningún usuario (por ejemplo, un logro global o sin asignar).
