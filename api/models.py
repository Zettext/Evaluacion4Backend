from django.db import models

class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Sensor(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('bloqueado', 'Bloqueado'),
        ('perdido', 'Perdido'),
    ]
    #mac unica
    mac_address = models.CharField(max_length=50, unique=True, verbose_name="MAC Address")
    modelo = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='inactivo')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, related_name='sensores')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.modelo} - {self.mac_address}"

class Evento(models.Model):
    TIPOS = [
        ('entrada', 'Entrada Permitida'),
        ('salida', 'Salida Registrada'),
        ('denegado', 'Acceso Denegado'),
        ('error', 'Error de Lectura'),
    ]
    
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.fecha_registro}"