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
        # 1. Limpieza básica
        nombre = value.strip()
        
        # 2. Longitud mínima
        if len(nombre) < 3:
            raise serializers.ValidationError("El nombre es muy corto (mínimo 3 letras).")

        # 3. Formato (Solo letras, números y espacios - Sin símbolos raros)
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\-\.]+$', nombre):
            raise serializers.ValidationError("El nombre contiene caracteres inválidos. Use solo letras, números y espacios.")

        # 4. Unicidad (Evitar duplicados tipo "Bodega" y "bodega")
        # Si estamos creando (no hay self.instance) o actualizando (cambiando el nombre)
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
        # 1. Formato estricto XX:XX:XX:XX:XX:XX (Hexadecimal)
        patron_mac = r'^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$'
        if not re.match(patron_mac, value):
            raise serializers.ValidationError("Formato inválido. Debe ser XX:XX:XX:XX:XX:XX (ej: AA:BB:CC:11:22:33)")
        
        return value.upper() # Lo guardamos siempre en mayúsculas para ordenar

    def validate_modelo(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El modelo debe tener al menos 3 caracteres.")
        
        # Evitar caracteres peligrosos como <script> o $
        if re.search(r'[<>${};]', value):
            raise serializers.ValidationError("El modelo contiene caracteres no permitidos.")
            
        return value.strip()

    # VALIDACIÓN GLOBAL (Relación entre campos)
    def validate(self, data):
        estado = data.get('estado')
        departamento = data.get('departamento')

        # Regla 1: Un sensor ACTIVO debe tener departamento
        if estado == 'activo' and not departamento:
            raise serializers.ValidationError({
                "estado": "No se puede activar el sensor sin asignarlo a un departamento."
            })
        
        # Regla 2: Un sensor PERDIDO no debería tener departamento asignado (opcional, pero profesional)
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