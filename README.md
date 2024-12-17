# sistema-tareas-gamificado



# DESCRIPCIÓN DE MODELOS.
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


# 2. Usuario
El modelo Usuario representa a un usuario dentro de la aplicación. Contiene información básica sobre el usuario, como su nombre, correo electrónico y nivel. Este modelo se utiliza para gestionar a los usuarios en la aplicación y asociarles tareas o logros, pero no se utiliza para el login de la aplicación.

# Campos:
# nombre (CharField):
Tipo: CharField
Descripción: Almacena el nombre del usuario. Este campo se utiliza para identificar al usuario dentro de la aplicación, especialmente cuando se asocian tareas, logros u otras interacciones con el usuario.
Longitud máxima: 255 caracteres.

# correo (CharField):
Tipo: CharField
Descripción: Almacena la dirección de correo electrónico del usuario. Este campo puede ser utilizado para comunicaciones o para fines administrativos, pero no está relacionado con el inicio de sesión en la aplicación.
Longitud máxima: 255 caracteres.


# nivel (PositiveIntegerField):
Tipo: PositiveIntegerField
Descripción: Representa el nivel o el rango del usuario dentro de la aplicación. Este campo indica el progreso o la experiencia del usuario, con un valor predeterminado de 1 y que puede aumentar conforme el usuario complete ciertas tareas o logros.
Valor por defecto: 1.






# 3. Tareas
El modelo Tareas representa a una tarea dentro de la aplicación. Contiene información básica sobre el , como su nombre, correo electrónico y nivel. Este modelo es esencial para gestionar a los usuarios en la aplicación, permitiendo almacenar y acceder a sus datos.




# Descripción De Endpoints.