from django.shortcuts import render
from django.http import HttpResponse
<<<<<<< HEAD
=======
from asistencia.models import Ugel  # Reemplaza por el nombre exacto de tu modelo

>>>>>>> 4077843d802b1ccc565f83da5322f2e60666180f

def inicio_index(request):
    """
    Vista principal del sistema.
    Los datos de la UGEL no necesitan pasarse manualmente aquí 
    porque el Context Processor 'ugel_context' los inyecta automáticamente a base.html.
    """
<<<<<<< HEAD
    context = {
        'mantenimiento_activo': False  # Asegura que el menú esté 100% activo
=======
    ugel_data = Ugel.objects.first()
    context = {
        'ugel': ugel_data,
>>>>>>> 4077843d802b1ccc565f83da5322f2e60666180f
    }
    return render(request, 'inicio/index.html', context)
