# asistencia/views/instituciones_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.db import IntegrityError
from ..models import Institucion
from ..forms import InstitucionForm

def institucion_listar(request):
    instituciones = _filtrar_instituciones(request)
    paginator = Paginator(instituciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'titulo_seccion': 'Tabla Instituciones',
        'nombre_singular': 'Institución',
        'campo_busqueda': 'nombre o código modular',
        'url_crear': 'institucion_crear',
        'mantenimiento_activo': False,
    }
    return render(request, 'instituciones/listar.html', context)

def institucion_crear(request):
    if request.method == 'POST':
        form = InstitucionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'La Institución se registró correctamente.')
            return redirect('institucion_listar')
    else:
        form = InstitucionForm()
        
    context = {
        'form': form,
        'mantenimiento_activo': True,
    }
    return render(request, 'instituciones/crear.html', context)

def institucion_editar(request, pk):
    institucion = get_object_or_404(Institucion, pk=pk)
    if request.method == 'POST':
        form = InstitucionForm(request.POST, instance=institucion)
        if form.is_valid():
            form.save()
            messages.success(request, f'La Institución "{institucion.nombre}" fue actualizada.')
            return redirect('institucion_listar')
    else:
        form = InstitucionForm(instance=institucion)
        
    context = {
        'form': form,
        'titulo_formulario': f'Editar Institución: {institucion.nombre}',
        'mantenimiento_activo': True,
    }
    return render(request, 'instituciones/form.html', context)

def institucion_anular(request, pk):
    if request.method == 'POST':
        institucion = get_object_or_404(Institucion, pk=pk)
        try:
            nombre = institucion.nombre
            institucion.delete()
            messages.success(request, f'La institución "{nombre}" fue eliminada permanentemente.')
        except (ProtectedError, IntegrityError):
            institucion.estado = False
            institucion.save()
            messages.warning(request, f'La institución "{institucion.nombre}" está vinculada. Se cambió su estado a Inactivo.')
    return redirect('institucion_listar')

def _filtrar_instituciones(request):
    query = request.GET.get('q', '')
    filtro = request.GET.get('filtro', '')
    instituciones = Institucion.objects.select_related('turno', 'distrito').all().order_by('-id')
    
    if query:
        instituciones = instituciones.filter(nombre__icontains=query) | instituciones.filter(codigo_modular__icontains=query)
    if filtro == 'activos':
        instituciones = instituciones.filter(estado=True)
    elif filtro == 'inactivos':
        instituciones = instituciones.filter(estado=False)
        
    return instituciones
