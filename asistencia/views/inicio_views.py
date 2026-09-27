from django.shortcuts import render
from django.http import HttpResponse
from asistencia.models import Ugel

def inicio_index(request):
    """
    Vista principal del sistema.
    """
    try:
        ugel_real = Ugel.objects.first()
    except Exception:
        ugel_real = None

    context = {
        'mantenimiento_activo': False,
        'ugel': ugel_real
    }
    return render(request, 'inicio/index.html', context)
