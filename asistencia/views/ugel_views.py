from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Ugel
from ..forms import UgelForm

def ugel_mantenimiento(request):
    ugel_obj = Ugel.objects.first()
    
    if request.method == 'POST':
        form = UgelForm(request.POST, request.FILES, instance=ugel_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información de la UGEL actualizada correctamente.')
            return redirect('inicio')  # Redirige a la ruta con name='inicio'
    else:
        form = UgelForm(instance=ugel_obj)

    context = {
        'form': form,
        'mantenimiento_activo': True,
        'titulo_tabla': 'Configuración de Tabla UGEL'
    }
    return render(request, 'ugel/mantenimiento.html', context)
