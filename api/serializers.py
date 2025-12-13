import re
from rest_framework import serializers
from .models import Departamento, Sensor, Evento

# ---------------------------------------------------------
# Serializer de DEPARTAMENTOS
# ---------------------------------------------------------
class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

    def validate_nombre(self, value):
        nombre = value.strip()
        
        #long minima
        if len(nombre) < 3:
            raise serializers.ValidationError("El nombre es muy corto (mínimo 3 letras).")

        # limpieza para el formato, *APRENDER COMO FUNCIONA* sinceramente el arreglo no lo hice yo.
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\-\.]+$', nombre):
            raise serializers.ValidationError("El nombre contiene caracteres inválidos. Use solo letras, números y espacios.")

        #revisar si existe para q no hayan duplicados
        existe = Departamento.objects.filter(nombre__iexact=nombre)
        if self.instance:
            existe = existe.exclude(pk=self.instance.pk)
        
        if existe.exists():
            raise serializers.ValidationError(f"Ya existe un departamento llamado '{nombre}'.")

        return nombre

    def validate_descripcion(self, value):
        if value and len(value.strip()) < 5:
            raise serializers.ValidationError("La descripción es demasiado breve.")
        return value


# ---------------------------------------------------------
# Serializer de SENSORES (Validaciones Estrictas)
# ---------------------------------------------------------
class SensorSerializer(serializers.ModelSerializer):
    # Campo extra para mostrar el nombre del departamento en lugar de solo el ID al leer
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)

    class Meta:
        model = Sensor
        fields = '__all__'

    def validate_mac_address(self, value):
        # nuevamente, aprender el formato
        patron_mac = r'^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$'
        if not re.match(patron_mac, value):
            raise serializers.ValidationError("Formato inválido. Debe ser XX:XX:XX:XX:XX:XX (ej: AA:BB:CC:11:22:33)")
        
        return value.upper() #mayusculas siempre 

    #nuevamente, que tenga por lo menos 3 caracteres
    def validate_modelo(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El modelo debe tener al menos 3 caracteres.")
        
        #ARREGLO PARA EVITAR SIMBOLOS NO UTILES
        if re.search(r'[<>${};]', value):
            raise serializers.ValidationError("El modelo contiene caracteres no permitidos.")
            
        return value.strip()#terminar de limpiar

    # VALIDACIÓN GLOBAL (Relación entre campos)
    def validate(self, data):
        estado = data.get('estado')
        departamento = data.get('departamento')

        # Regla 1: Un sensor ACTIVO debe tener departamento
        if estado == 'activo' and not departamento:
            raise serializers.ValidationError({
                "estado": "No se puede activar el sensor sin asignarlo a un departamento."
            })
        
        # Regla 2: Un sensor PERDIDO no debería tener departamento asignado
        if estado == 'perdido' and departamento:
            raise serializers.ValidationError({
                "estado": "Un sensor declarado como 'perdido' no puede estar asignado a un departamento."
            })

        return data


# ---------------------------------------------------------
# Serializer de EVENTOS (Lógica de Negocio)
# ---------------------------------------------------------
class EventoSerializer(serializers.ModelSerializer):
    sensor_info = serializers.CharField(source='sensor.__str__', read_only=True)

    class Meta:
        model = Evento
        fields = '__all__'

    def validate_sensor(self, value):
        # Regla profesional: No registrar eventos de sensores bloqueados o perdidos
        if value.estado in ['bloqueado', 'perdido']:
            raise serializers.ValidationError(f"El sensor {value.mac_address} está en estado '{value.estado}' y no puede registrar eventos.")
        return value

    def validate_descripcion(self, value):
        if not value.strip():
            raise serializers.ValidationError("La descripción del evento no puede estar vacía.")
        return value