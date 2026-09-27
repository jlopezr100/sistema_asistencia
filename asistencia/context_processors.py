from .models import Ugel

def ugel_context(request):
    """
    Inyecta los datos de la UGEL globalmente en todas las plantillas.
    """
    try:
        ugel_data = Ugel.objects.first()
    except Exception:
        ugel_data = None

    return {
        'ugel': ugel_data
    }
