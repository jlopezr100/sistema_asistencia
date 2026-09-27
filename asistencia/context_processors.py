from .models import Ugel

def ugel_context(request):
    """
    Inyecta los datos de la UGEL globalmente en todas las plantillas.
    """
    try:
        # Intentamos obtener el primer registro guardado en la base de datos de Aiven
        ugel_data = Ugel.objects.first()
    except Exception:
        ugel_data = None

    # Si la base de datos está vacía, retornamos un diccionario plano pero compatible
    if not ugel_data:
        return {
            'ugel': {
                'nombre': 'UGEL por Configurar',
                'ruc': '---',
                'direccion': 'No registrada',
                'correo': 'contacto@ugel.gob.pe',
                'telefono': '---',
                'eslogan': None,
                'quienes_somos': None,
                'mision': None,
                'vision': None,
                'logo': None
            }
        }
        
    # Si encuentra los datos reales de Aiven, inyecta el objeto real
    return {
        'ugel': ugel_data
    }
