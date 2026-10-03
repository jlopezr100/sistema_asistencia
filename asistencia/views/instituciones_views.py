# asistencia/views/instituciones_views.py
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.db import IntegrityError
from django.http import HttpResponse
from django.template.loader import render_to_pdf # O la librería de PDF usada en tu proyecto (xhtml2pdf / reportlab)
from ..models import Institucion, Ugel
from ..forms import InstitucionForm

def _filtrar_instituciones(request):
    query = request.GET.get('q', '').strip()
    filtro = request.GET.get('filtro', '')
    instituciones = Institucion.objects.select_related('turno', 'distrito').all().order_by('-id')
    
    if query:
        # Búsqueda por Código Modular, Nombre o Distrito
        instituciones = instituciones.filter(
            Q(codigo_modular__icontains=query) |
            Q(nombre__icontains=query) |
            Q(distrito__nombre__icontains=query)
        )
    if filtro == 'activos':
        instituciones = instituciones.filter(estado=True)
    elif filtro == 'inactivos':
        instituciones = instituciones.filter(estado=False)
        
    return instituciones

def institucion_listar(request):
    instituciones = _filtrar_instituciones(request)
    paginator = Paginator(instituciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'titulo_seccion': 'Tabla Instituciones',
        'nombre_singular': 'Institución',
        'campo_busqueda': 'código modular, nombre o distrito',
        'url_crear': 'institucion_crear',
        'url_pdf': 'institucion_pdf',
        'url_excel': 'institucion_excel',
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

# --- REPORTE EXCEL ---
def institucion_exportar_excel(request):
    instituciones = _filtrar_instituciones(request)
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Instituciones"
    
    # Encabezados
    headers = ['ID', 'CÓDIGO MODULAR', 'NOMBRE DE LA I.E.', 'DISTRITO', 'TURNO', 'ESTADO']
    ws.append(headers)
    
    # Estilos de Encabezado
    fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    font = Font(color="FFFFFF", bold=True)
    for cell in ws[1]:
        cell.fill = fill
        cell.font = font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    # Datos
    for inst in instituciones:
        ws.append([
            inst.id,
            inst.codigo_modular,
            inst.nombre,
            inst.distrito.nombre if inst.distrito else '',
            inst.turno.nombre if inst.turno else '',
            'ACTIVO' if inst.estado else 'INACTIVO'
        ])
        
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Reporte_Instituciones.xlsx"'
    wb.save(response)
    return response

# --- REPORTE PDF ---
def institucion_reporte_pdf(request):
    instituciones = _filtrar_instituciones(request)
    ugel = Ugel.objects.first()
    
    context = {
        'instituciones': instituciones,
        'ugel': ugel,
        'titulo': 'REPORTE DE INSTITUCIONES EDUCATIVAS'
    }
    # Asegúrate de tener configurada tu función utilitaria render_to_pdf o usar xhtml2pdf
    return render(request, 'instituciones/reporte_pdf.html', context)

