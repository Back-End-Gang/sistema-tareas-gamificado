from django.shortcuts import render
from logros.models import Logro
from django.http import JsonResponse
from LogrosGamificadoAPI.serializers import LogroSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def logros_list(request):
    if request.method == 'GET':
        logro = Logro.objects.all()
        serializer = LogroSerializer(logro, many=True)
        return Response(serializer.data)  # Aquí eliminamos safe=False
    
    if request.method == 'POST':
        serializer = LogroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST', 'DELETE'])
def logros_detail(request, pk):
    try:
        logro = Logro.objects.get(pk=pk)
    except Logro.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LogroSerializer(logro)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = LogroSerializer(logro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        logro.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)