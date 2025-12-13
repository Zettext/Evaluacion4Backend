from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Departamento, Sensor, Evento
from .serializers import DepartamentoSerializer, SensorSerializer, EventoSerializer

#para el error personalizado
from django.http import Http404
from rest_framework.exceptions import NotFound
from django.http import JsonResponse

#endpoint publico
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

#Viewset protegido con token
class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAdminUser]# Solo admin

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound("El recurso solicitado no existe o fue eliminado.\nPor favor, borra la cuenta")

#solo operadores ver y admin hacer acciones
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        #permitir menos opciones a alguien 
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # POST, PUT, DELETE solo para Admin
        return request.user and request.user.is_staff
    
#Viewset protegido con token
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdminOrReadOnly]# Solo usuarios logueados

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound("El recurso solicitado no existe o fue eliminado.\nPor favor, borra la cuenta")

#Viewset protegido con token
class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]# Solo usuarios logueados

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound("El recurso solicitado no existe o fue eliminado.\nPor favor, borra la cuenta")
        
def custom_404(request, exception):
    return JsonResponse({
        "status_code": 404,
        "error_type": "RouteNotFound",
        "detail": "La ruta URL solicitada no existe en esta API. Verifica el endpoint."
    }, status=404)

