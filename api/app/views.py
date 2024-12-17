import json
import traceback
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from app.models import Registro
from app.serializers import RegistroSerializer

@api_view(['POST'])
def criar_registro(request):
    try:
        items = request.data['data']
        for item in items:
            Registro.objects.create(
                timestamp = float(item['timestamp']),
                velocidade = float(item['velocidade'])
            )
        return Response({"detail":f"{len(items)} items adicionados"}, status = status.HTTP_201_CREATED)
    except: 
        print({"error":f"{traceback.format_exc()}"})
        return Response({"error":f"{traceback.format_exc()}"}, status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def listar_registros(request):
    registros = Registro.objects.all()
    serializer = RegistroSerializer(registros,many = True)
    return Response(serializer.data,status = status.HTTP_200_OK)


@api_view(['POST'])
def listar_registros_a_partir_de_timestamp(request):
    try:

        timestamp = float(request.data['timestamp'])
        registros = Registro.objects.filter(timestamp__gte=timestamp)
        items = []
        for item in registros:
            items.append({
                "timestamp": item.timestamp,
                "velocidade": item.velocidade
            })
        return Response(items, status = status.HTTP_200_OK)
    except Exception as ex:
        print(traceback.format_exc())
        return Response({
            "error":f"{traceback.format_exc()}"
            },status= status.HTTP_400_BAD_REQUEST)
