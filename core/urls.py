from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import DepartamentoViewSet, SensorViewSet, EventoViewSet, api_info, custom_404

router = DefaultRouter()
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'sensores', SensorViewSet)
router.register(r'eventos', EventoViewSet)

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),
    
    # RUTAS PARA EL TOKEN
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    #informacion, publica
    path('api/info/', api_info, name='api_info'),

    #router para no tener que hacer mil api/algo naajja
    path('api/', include(router.urls)),
]

handler404 = custom_404