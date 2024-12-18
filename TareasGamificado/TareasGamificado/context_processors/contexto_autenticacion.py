def estado_autenticacion(request):
    return {'autenticado': getattr(request, 'autenticado', False)}