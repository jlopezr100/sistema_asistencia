from .models import Ugel

def ugel_context(request):
    """
    Inyecta los datos de la UGEL globalmente de forma limpia y directa.
    """
    try:
        # Buscamos el registro ID 1 que ya existe en Aiven
        ugel_data = Ugel.objects.first()
    except Exception:
        ugel_data = None

    return {
        'ugel': ugel_data
    }
