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

    # Validación por campo: Nombre
    def validate_nombre(self, value):
        # Evitar nombres vacíos o de espacios en blanco
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre del departamento debe tener al menos 3 letras.")
        
        # Evitar caracteres extraños (opcional, solo letras y espacios)
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras y espacios.")
        
        return value

# ---------------------------------------------------------
# Serializer de SENSORES (El más importante)
# ---------------------------------------------------------
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

    # 1. Validación por campo: Modelo
    def validate_modelo(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El modelo debe tener al menos 3 caracteres.")
        return value

    # 2. Validación por campo: MAC Address (Formato estricto)
    def validate_mac_address(self, value):
        # Regex para validar formato XX:XX:XX:XX:XX:XX (Hexadecimal)
        patron_mac = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        
        if not re.match(patron_mac, value):
            raise serializers.ValidationError("La dirección MAC no es válida. Use el formato XX:XX:XX:XX:XX:XX")
        
        return value

    # 3. Validación GLOBAL (Cruza dos o más campos)
    # Requisito explícito de la rúbrica: "validaciones globales"
    def validate(self, data):
        # Regla de negocio: Un sensor no puede estar "activo" si no tiene un departamento asignado.
        estado = data.get('estado')
        departamento = data.get('departamento')

        # Si estamos creando (POST) o actualizando (PUT) y falta el departamento
        if estado == 'activo' and not departamento:
            raise serializers.ValidationError({
                "estado": "No puedes activar un sensor si no está asignado a un departamento."
            })
        
        return data

# ---------------------------------------------------------
# Serializer de EVENTOS
# ---------------------------------------------------------
class EventoSerializer(serializers.ModelSerializer):
    sensor_detalle = serializers.CharField(source='sensor.modelo', read_only=True)

    class Meta:
        model = Evento
        fields = '__all__'

    # Validación por campo: Tipo de evento
    def validate_tipo(self, value):
        tipos_validos = ['entrada', 'salida', 'denegado', 'error']
        if value not in tipos_validos:
            raise serializers.ValidationError(f"El tipo de evento no es válido. Opciones: {tipos_validos}")
        return value