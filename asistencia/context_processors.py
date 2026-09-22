from .models import Ugel

def ugel_context(request):
    """
    Inyecta los datos de la UGEL globalmente en todas las plantillas.
    """
    ugel_data = Ugel.objects.first()
    return {
        'ugel': ugel_data
    }
