from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from asistencia.models import Maquina
from ..forms import MaquinaForm

# 1. Listado (Apunta a listar.html)
def maquina_listar(request):
    maquinas = Maquina.objects.all()
    return render(request, 'maquina/listar.html', {'maquinas': maquinas})

# 2. Crear (Usa form.html)
def maquina_crear(request):
    if request.method == 'POST':
        form = MaquinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maquina_listar')
    else:
        form = MaquinaForm()
    
    return render(request, 'maquina/form.html', {
        'form': form,
        'titulo_formulario': 'Registrar Nueva Máquina',
        'mantenimiento_activo': True  # <-- Habilita el bloqueo del menú
    })

def maquina_editar(request, pk):
    maquina = get_object_or_404(Maquina, pk=pk)
    if request.method == 'POST':
        form = MaquinaForm(request.POST, instance=maquina)
        if form.is_valid():
            form.save()
            return redirect('maquina_listar')
    else:
        form = MaquinaForm(instance=maquina)
    
    return render(request, 'maquina/form.html', {
        'form': form,
        'maquina': maquina,
        'titulo_formulario': f'Editar Máquina: {maquina.serie_dispositivo}',
        'mantenimiento_activo': True  # <-- Habilita el bloqueo del menú
    })

# 4. Eliminar
def maquina_eliminar(request, pk):
    maquina = get_object_or_404(Maquina, pk=pk)
    if request.method == 'POST':
        maquina.delete()
        return redirect('maquina_listar')
    return render(request, 'maquina/eliminar.html', {'maquina': maquina})

# 5. Validación AJAX
def verificar_unicidad_maquina(request):
    serie = request.GET.get('serie', '').strip()
    maquina_id = request.GET.get('id', None)

    qs = Maquina.objects.filter(serie_dispositivo__iexact=serie)
    if maquina_id:
        qs = qs.exclude(id=maquina_id)

    existe = qs.exists()
    return JsonResponse({'existe': existe})
