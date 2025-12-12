from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import DepartamentoViewSet, SensorViewSet, EventoViewSet, api_info

# El Router crea las rutas del CRUD automáticamente
router = DefaultRouter()
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'sensores', SensorViewSet)
router.register(r'eventos', EventoViewSet)

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),
    
    # Rutas para el Login (JWT)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),     # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    # Refrescar token
    
    # Endpoint de Información (Requerimiento PDF)
    path('api/info/', api_info, name='api_info'),
    
    # Rutas automáticas de la API (sensores, departamentos, eventos)
    path('api/', include(router.urls)),
]