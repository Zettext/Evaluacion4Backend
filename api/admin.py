from django.contrib import admin
from .models import Departamento, Sensor, Evento

admin.site.register(Departamento)
admin.site.register(Sensor)
admin.site.register(Evento)