from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, NotFound, PermissionDenied, NotAuthenticated, ValidationError
from django.http import Http404

def custom_exception_handler(exc, context):
    #el DRF maneja el error primero
    response = exception_handler(exc, context)

    # Si hubo una respuesta (es un error conocido por DRF), la personalizamos
    if response is not None:
        
        # Estructura base profesional 
        custom_data = {
            "status_code": response.status_code,
            "error_type": exc.__class__.__name__,
            "detail": "Ha ocurrido un error en la solicitud."
        }

        #Error 401
        if isinstance(exc, NotAuthenticated):
            custom_data["detail"] = "No estás autenticado. OJO CON EL TOKEN."

        #Error 403
        elif isinstance(exc, PermissionDenied):
            custom_data["detail"] = "Acceso denegado. No tienes permisos suficientes para realizar esta acción."

        #Error 404
        elif isinstance(exc, (NotFound, Http404)):
            custom_data["detail"] = "El recurso solicitado no existe o fue eliminado."

        #Error 400
        elif isinstance(exc, ValidationError):
            custom_data["detail"] = "Error de validación. Revisa los datos enviados."
            # En validaciones, agregamos los campos específicos que fallaron
            custom_data["campos_con_error"] = response.data

        # Reemplazamos la data original por nuestra data personalizada
        response.data = custom_data

    return response