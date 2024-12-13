from django.shortcuts import render
from tareas.models import Tarea
from django.http import JsonResponse
from TareasGamificadoAPI.serializers import TareaSerializar
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET', 'POST'])
def tarea_list(request):
    if request.method == 'GET':
        tarea = Tarea.objects.all()
        serializer = TareaSerializar(tarea, many=True)
        return Response(serializer.data)  # Aquí eliminamos safe=False
    
    if request.method == 'POST':
        serializer = TareaSerializar(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def tarea_detail(request, pk):
    try:
        tarea = Tarea.objects.get(pk=pk)
    except Tarea.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TareaSerializar(tarea)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = TareaSerializar(tarea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        tarea.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)