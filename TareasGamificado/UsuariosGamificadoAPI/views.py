from django.shortcuts import render
from usuarios.models import Usuario
from django.http import JsonResponse
from UsuariosGamificadoAPI.serializers import UsuarioSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def usuarios_list(request):
    if request.method == 'GET':
        usuario = Usuario.objects.all()
        serializer = UsuarioSerializers(usuario, many=True)
        return Response(serializer.data)  # Aquí eliminamos safe=False
    
    if request.method == 'POST':
        serializer = UsuarioSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST', 'DELETE'])
def usuarios_detail(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UsuarioSerializers(usuario)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = UsuarioSerializers(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        usuario.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)