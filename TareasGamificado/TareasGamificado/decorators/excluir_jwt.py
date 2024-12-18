from functools import wraps

# Decorador para excluir vistas del middleware o para saltar una vista/página del proceso de autenticación. Usado sólo para la vista base que no utiliza autenticación basada en token JWT
def excluido_jwt(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        setattr(request, '_skip_authenticated_user', True)
        return view_func(request, *args, **kwargs)
    return _wrapped_view