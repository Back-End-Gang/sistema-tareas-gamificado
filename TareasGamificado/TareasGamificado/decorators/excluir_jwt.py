from functools import wraps

# Decorador para excluir vistas del middleware
def excluido_jwt(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        setattr(request, '_skip_authenticated_user', True)
        return view_func(request, *args, **kwargs)
    return _wrapped_view