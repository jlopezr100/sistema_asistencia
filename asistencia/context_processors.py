from .models import Ugel

def ugel_context(request):
    """
    Inyecta los datos de la UGEL globalmente en todas las plantillas de forma segura.
    """
    try:
        ugel_data = Ugel.objects.first()
    except Exception:
        ugel_data = None

    # Si la base de datos está vacía y no hay registros, creamos un diccionario temporal
    if not ugel_data:
        return {
            'ugel': {
                'nombre': 'UGEL por Configurar',
                'siglas': 'UGEL',
                'logo': None
            }
        }
        
    return {
        'ugel': ugel_data
    }
