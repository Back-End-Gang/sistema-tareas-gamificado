# Sistema-tareas-gamificado

# Documentación de instalación y pasos para ejecutar

## Requerimeintos y dependencias:

Django==5.1.1
djangorestframework==3.15.2
djangorestframework_simplejwt==5.3.1
PyJWT==2.10.1
PyJWT==2.10.1
Pip Install Requirements.txt in Python
Pasos para usar pip install con requirements.txt:

## Asegurarse de tener Python instalado

Verificar que Python esté instalado ejecutando el siguiente comando en tu terminal (Windows+R y escribir cmd):
python --version

Si usas sistemas basados en Unix (Linux o Mac) o tienes varias versiones de Python instaladas, puede que necesites usar:
python3 --version

En Windows:
venv\Scripts\activate

En Linux/Mac:
source venv/bin/activate

## Navegar al directorio donde está tu archivo requirements.txt

Usa el comando cd para acceder al directorio raíz del proyecto donde se encuentra el archivo requirements.txt:
Ejemplo de ruta: C:/Usuarios/admin/Documentos/GitHub/sistema-tareas-gamificado
cd ruta/al/directorio

## Ejecutar el comando para instalar las dependencias

Usa pip para instalar todas las librerías listadas en el archivo requirements.txt:
pip install -r requirements.txt
Verifica que las librerías se instalaron correctamente

## Listar las librerías instaladas para confirmar

pip list
Ejecuta tu proyecto
Después de instalar las dependencias, puedes proceder con los comandos necesarios para ejecutar tu proyecto.

## Crear Super Usuario

python manage.py createsuperuser

pasos
1.-Colocar nombre de usuario.
2.-Colocar Contraseña.
3.-Reingresar Contraseña.

## Realizar migraciones

En la terminal integrada de VSCode, ejecutar el comando (en la carpeta que contiene el archivo manage.py) python manage.py makemigrations
Después, ejecutar en la misma ruta el comando python manage.py migrate

## Abrir Visual Studio Code y ejecutar el programa

- Ir a ejecutar y depurar (ícono de reproducción con un bicho)
- Si es necesario, seleccionar Django como el configurador de ejecución
- Presionar en el botón para comenzar a depurar
- Esperar a que inicie el programa
- Ir a la dirección web http://127.0.0.1:8000/

# Documentación del Funcionamiento del Sistema

## DESCRIPCIÓN DE MODELOS.
### 1. Logro
El modelo Logro representa un logro que se asocia a un usuario dentro de la aplicación. Puede ser utilizado para registrar cualquier tipo de éxito, tarea completada o meta alcanzada por un usuario.

### Campos:
#### nombre(CharField):
Tipo: CharField
Descripción: El nombre o título del logro. Este campo almacena una breve descripción del logro, como por ejemplo: "Usuario del mes", "Nivel completado", etc.
Longitud máxima: 100 caracteres.

#### descripcion (TextField):
Tipo: TextField
Descripción: Un campo de texto donde se describe en detalle el logro. Este campo puede contener información más detallada sobre el logro, por ejemplo cómo se alcanzó, los pasos seguidos o el impacto del logro.

#### usuario (ForeignKey):
Tipo: ForeignKey
Descripción: Este campo establece una relación con el modelo Usuario, lo que significa que cada logro está vinculado a un usuario específico.
Comportamiento en caso de eliminación: Cuando un usuario es eliminado, este campo se establece en NULL (on_delete=models.SET_NULL), lo que garantiza que los logros no sean eliminados junto con el usuario.
null=True: Permite que este campo pueda ser nulo, es decir, un logro puede no estar asociado a ningún usuario (por ejemplo, un logro global o sin asignar).


### 2. Usuario
El modelo Usuario representa a un usuario dentro de la aplicación. Contiene información básica sobre el usuario, como su nombre, correo electrónico y nivel. Este modelo se utiliza para gestionar a los usuarios en la aplicación y asociarles tareas o logros, pero no se utiliza para el login de la aplicación.

### Campos:
#### nombre (CharField):
Tipo: CharField
Descripción: Almacena el nombre del usuario. Este campo se utiliza para identificar al usuario dentro de la aplicación, especialmente cuando se asocian tareas, logros u otras interacciones con el usuario.
Longitud máxima: 255 caracteres.

#### correo (CharField):
Tipo: CharField
Descripción: Almacena la dirección de correo electrónico del usuario. Este campo puede ser utilizado para comunicaciones o para fines administrativos, pero no está relacionado con el inicio de sesión en la aplicación.
Longitud máxima: 255 caracteres.


#### nivel (PositiveIntegerField):
Tipo: PositiveIntegerField
Descripción: Representa el nivel o el rango del usuario dentro de la aplicación. Este campo indica el progreso o la experiencia del usuario, con un valor predeterminado de 1 y que puede aumentar conforme el usuario complete ciertas tareas o logros.
Valor por defecto: 1.


### 3. Tareas
El modelo de Tarea se usa para representar las actividades o acciones que un usuario puede realizar dentro de la app. Cada tarea tiene un título, una descripción, un estado, una cantidad de puntos y está asociada a un usuario en particular. Sirve para llevar el control de las tareas pendientes, completadas o cualquier cosa que el usuario deba hacer dentro de la plataforma.

### Campos:
#### titulo (CharField):
Tipo: CharField
Descripción: Almacena el título o nombre corto de la tarea. Este campo describe brevemente el propósito de la tarea, por ejemplo, "Completar nivel 1", "Enviar reporte", etc.
Longitud máxima: 100 caracteres.

#### descripcion (TextField):
Tipo: TextField
Descripción: Este campo almacena una descripción más detallada de la tarea, explicando los pasos a seguir, el contexto de la tarea, o cualquier otro detalle importante que el usuario deba conocer.

#### estado (CharField):
Tipo: CharField
Descripción: Define el estado de la tarea. Utiliza una lista de opciones predefinidas que indican si la tarea está "pendiente" o "completada".
Opciones:
'pendiente': La tarea aún no se ha completado.
'completada': La tarea ha sido completada.
Valor por defecto: 'pendiente'.
Longitud máxima: 20 caracteres.

#### puntos (PositiveIntegerField):
Tipo: PositiveIntegerField
Descripción: Representa la cantidad de puntos asociados a la tarea. Este campo puede usarse para valorar la tarea según su dificultad o importancia.
Valor por defecto: 1.
Restricción: Solo se permiten valores enteros positivos (mayores que cero).

#### usuario (ForeignKey):
Tipo: ForeignKey
Descripción: Este campo establece una relación con el modelo Usuario, lo que significa que cada tarea está vinculada a un usuario específico.
Comportamiento en caso de eliminación: Si un usuario es eliminado, las tareas asociadas a este se establecerán en NULL (es decir, el campo usuario quedará vacío).
null=True: Permite que este campo pueda ser nulo, lo que indica que una tarea puede no estar asociada a ningún usuario.

# Descripción De Endpoints.
La estructura básica de tus endpoints incluye:

- URL: La ruta específica a la que se envía una solicitud.
- Método HTTP: El tipo de acción que se ejecuta (POST, GET, PUT/PATCH, DELETE).
- Vista Asociada: La clase o función que maneja la lógica del endpoint.
- Descripción: Qué hace el endpoint (funcionalidad).
- Descripción de los Endpoints.

## Endpoints de Autenticación
URL	              Método	Vista Asociada	 Descripción
/	              GET	    Home	         Muestra la página de inicio de la API.
/accounts/login/  POST	    VistaLogin	     Realiza el login del usuario.
/accounts/logout/ POST	    VistaLogout	     Cierra la sesión del usuario.
/token/	          POST	    VistaCrearToken	 Vista de desarrollador para generar un nuevo token.
/token/refresh/	  POST	    TokenRefreshView Vista de desarrollador para refrescar el token existente.

## Endpoints para Tareas
URL	                        Método	 Vista Asociada	 Descripción
/crear_tarea/	            POST	 TareaCrear	     Crea una nueva tarea en la base de datos desde la API.
/listar_tareas/	            GET	     TareaListar	 Extrae todos los datos del sistema para mostrarlos en una vista API.
/actualizar_tarea/<int:pk>/	PUT	     TareaEditar	 Actualiza una tarea específica por su ID.
/eliminar_tarea/<int:pk>/	DELETE	 TareaEliminar	 Elimina una tarea específica por su ID.

## Endpoints para Usuarios
URL	                            Método	Vista Asociada	Descripción
/crear_usuario/	                POST	UsuarioCrear	Crea un nuevo usuario.
/listar_usuarios/	            GET	    UsuarioListar	Extrae todos los datos del sistema para mostrarlos en una vista API.
/actualizar_usuario/<int:pk>/	PUT	    UsuarioEditar	Actualiza un usuario específico por su ID.
/eliminar_usuario/<int:pk>/	    DELETE	UsuarioEliminar	Elimina un usuario específico por su ID.

## Endpoints para Logros
URL	                         Método	Vista Asociada	Descripción
/crear_logro/	             POST	LogroCrear	    Crea un nuevo logro.
/listar_logros/	             GET	LogroListar	    Extrae todos los datos del sistema para mostrarlos en una vista API.
/actualizar_logros/<int:pk>/ PUT	LogroEditar	    Actualiza un logro específico por su ID.
/eliminar_logros/<int:pk>/	 DELETE	LogroEliminar	Elimina un logro específico por su ID.

## Endpoints De Visualización Json
URL
tareas_lista_json/
tarea_json/<int:pk>/
usuario_lista_json/
usuario_json/<int:pk>/
logro_lista_json/
logro_json/<int:pk>/



# Métodos HTTP Utilizados
GET: Obtener datos.

# Ejemplos

Ejemplo: /listar_tareas/ devuelve todas las tareas.
POST: Crear datos.

Ejemplo: /crear_tarea/ crea una nueva tarea.
PUT: Actualizar datos completos.

Ejemplo: /actualizar_tarea/1/ actualiza todos los campos de una tarea con ID = 1.
DELETE: Eliminar datos.

Ejemplo: /eliminar_tarea/1/ elimina la tarea con ID = 1.
Parámetros en los Endpoints
<int:pk>: Representa el ID del data (Primary Key).
Ejemplo: /actualizar_tarea/3/ significa que se actualizará la tarea con ID = 3.
Ejemplo de Solicitud HTTP
