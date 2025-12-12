from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Departamento, Sensor, Evento
from .serializers import DepartamentoSerializer, SensorSerializer, EventoSerializer
#para el error personalizado
from django.http import Http404
from rest_framework.exceptions import NotFound

# 1. Endpoint obligatorio /api/info/ (Público, cualquiera puede verlo)
@api_view(['GET'])
@permission_classes([AllowAny]) 
def api_info(request):
    return Response({
        "autor": "Javier Sánchez Leiva",
        "asignatura": "Backend",
        "proyecto": "SmartConnect API",
        "descripcion": "API para gestión de sensores IoT y control de acceso",
        "version": "6.9"
    })

# 2. ViewSet para Departamentos (Protegido con Token)
class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated] # Solo usuarios logueados

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound("El recurso solicitado no existe o fue eliminado.\nPor favor, borra la cuenta")

# 3. ViewSet para Sensores (Protegido con Token)
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound("El recurso solicitado no existe o fue eliminado.\nPor favor, borra la cuenta")

# 4. ViewSet para Eventos (Protegido con Token)
class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound("El recurso solicitado no existe o fue eliminado.\nPor favor, borra la cuenta")