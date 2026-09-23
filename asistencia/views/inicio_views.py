from django.shortcuts import render
from django.http import HttpResponse
from asistencia.models import Ugel  # Reemplaza por el nombre exacto de tu modelo


def inicio_index(request):
    """
    Vista principal del sistema.
    Los datos de la UGEL no necesitan pasarse manualmente aquí 
    porque el Context Processor 'ugel_context' los inyecta automáticamente a base.html.
    """
    ugel_data = Ugel.objects.first()
    context = {
        'ugel': ugel_data,
    }
    return render(request, 'inicio/index.html', context)
