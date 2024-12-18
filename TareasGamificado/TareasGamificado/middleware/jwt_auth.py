from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
import jwt
from django.conf import settings

# Middleware para gestionar autenticación JWT (JSON Web Token) usando verificación de tokens y cookies
# Agrega headers de autorización a las peticiones si se encuentra un token válido en las cookies de la página enviando la petición
# Utilizado sólo en las páginas que utilicen autenticación JWT

class AutenticacionJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request): # Cualquier petición será interceptada para verificar autenticación
        request.autenticado = False # Asume que todas las peticiones no están autenticadas para posterior uso por el context_processor

        if 'Authorization' not in request.headers and 'access_token' in request.COOKIES:
            # Verifica si la página a la que se le hace la petición no existe el header de Autorización
            # Igualmente, verifica si la página desde donde se realiza la petición existe la cookie con el token de acceso
            access_token = request.COOKIES.get('access_token') # Extrae la cookie del token de acceso

            try:
                jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"]) # Decodifica el token para verificar su validez
                # request.META es un diccionario que almacena metadatos de headers, incluyendo los headers de autorización
                # Si es válido, se añade el header "Authorization Bearer {access_token}" al diccionario
                # Para mejor clarificación sobre funcionamiento, se recomienda usar Postman u otra extensión que permita gestionar headers de manera manual
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
                print(request.META['HTTP_AUTHORIZATION'])
                request.autenticado = True
            except jwt.ExpiredSignatureError: # Elimina el token en caso de haber expirado
                self.eliminar_token_invalido(request)
            except jwt.InvalidTokenError: # Elimina el token en caso de ser inválido
                self.eliminar_token_invalido(request)

        return self.get_response(request)

    # Elimina todas las cookies de autenticación que contengan tokens inválidos
    def eliminar_token_invalido(self, request):
        response = self.get_response(request)
        response.delete_cookie('access_token') # Token para iniciar sesión
        response.delete_cookie('refresh_token') # Token para renovar sesión caso de que haya expirado el token de acceso
        response.delete_cookie('csrftoken') # Token de CSRF para protección de formularios
        return response