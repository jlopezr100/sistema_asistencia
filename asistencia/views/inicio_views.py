from django.shortcuts import render
from django.http import HttpResponse

def inicio_index(request):
    """
    Vista principal del sistema.
    Los datos de la UGEL no necesitan pasarse manualmente aquí 
    porque el Context Processor 'ugel_context' los inyecta automáticamente a base.html.
    """
    context = {
        'mantenimiento_activo': False  # Asegura que el menú esté 100% activo
    }
    return render(request, 'inicio/index.html', context)
