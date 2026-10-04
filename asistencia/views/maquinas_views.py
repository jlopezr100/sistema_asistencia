import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from asistencia.models import Maquina, Institucion
from ..forms import MaquinaForm

# 1. Listado (Apunta a listar.html)
def maquina_listar(request):
    query = request.GET.get('q', '').strip()
    institucion_id = request.GET.get('institucion_id', '').strip()

    maquinas = Maquina.objects.all().select_related('institucion')

    # Filtrado por búsqueda de texto (serie o nombre de la I.E.)
    if query:
        maquinas = maquinas.filter(
            Q(serie_dispositivo__icontains=query) | 
            Q(institucion__nombre__icontains=query)
        )

    # Filtrado por combo de Institución
    if institucion_id:
        maquinas = maquinas.filter(institucion_id=institucion_id)

    instituciones = Institucion.objects.all()

    return render(request, 'maquina/listar.html', {
        'maquinas': maquinas,
        'instituciones': instituciones,
        'query': query,
        'mantenimiento_activo': True
    })

def maquina_crear(request):
    if request.method == 'POST':
        form = MaquinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Máquina registrada correctamente.')
            return redirect('maquina_listar')
    else:
        form = MaquinaForm()

    return render(request, 'maquina/form.html', {
        'form': form,
        'titulo_formulario': 'Registrar Nueva Máquina',
        'mantenimiento_activo': True
    })

def maquina_editar(request, pk):
    maquina = get_object_or_404(Maquina, pk=pk)
    if request.method == 'POST':
        form = MaquinaForm(request.POST, instance=maquina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Máquina actualizada correctamente.')
            return redirect('maquina_listar')
    else:
        form = MaquinaForm(instance=maquina)

    return render(request, 'maquina/form.html', {
        'form': form,
        'maquina': maquina,
        'titulo_formulario': f'Editar Máquina: {maquina.serie_dispositivo}',
        'mantenimiento_activo': True
    })

def maquina_eliminar(request, pk):
    maquina = get_object_or_404(Maquina, pk=pk)
    if request.method == 'POST':
        serie = maquina.serie_dispositivo
        maquina.delete()
        messages.success(request, f'La máquina "{serie}" fue eliminada correctamente.')
        return redirect('maquina_listar')
    return redirect('maquina_listar')

# 5. Validación AJAX
def verificar_unicidad_maquina(request):
    serie = request.GET.get('serie', '').strip()
    maquina_id = request.GET.get('id', None)

    qs = Maquina.objects.filter(serie_dispositivo__iexact=serie)
    if maquina_id:
        qs = qs.exclude(id=maquina_id)

    existe = qs.exists()
    return JsonResponse({'existe': existe})

# ==========================================
# EXPORTAR A PDF
# ==========================================
def maquina_exportar_pdf(request):
    query = request.GET.get('q', '').strip()
    institucion_id = request.GET.get('institucion_id', '').strip()

    maquinas = Maquina.objects.all().select_related('institucion')

    if query:
        maquinas = maquinas.filter(
            Q(serie_dispositivo__icontains=query) | 
            Q(institucion__nombre__icontains=query)
        )

    if institucion_id:
        maquinas = maquinas.filter(institucion_id=institucion_id)

    # Configuración de respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_maquinas.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    story = []
    styles = getSampleStyleSheet()

    # Estilos de texto
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#002B49'),
        alignment=1,  # Centrado
        spaceAfter=15
    )

    cell_header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.white,
        fontName='Helvetica-Bold',
        alignment=1
    )

    cell_body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#333333')
    )

    # Título
    story.append(Paragraph("REPORTE DE MÁQUINAS / DISPOSITIVOS", title_style))
    story.append(Spacer(1, 10))

    # Encabezados de la tabla
    data = [
        [
            Paragraph("ID", cell_header_style),
            Paragraph("Serie Dispositivo", cell_header_style),
            Paragraph("Institución Educativa", cell_header_style)
        ]
    ]

    # Filas de datos
    for m in maquinas:
        data.append([
            Paragraph(str(m.id), cell_body_style),
            Paragraph(m.serie_dispositivo, cell_body_style),
            Paragraph(m.institucion.nombre if m.institucion else "-", cell_body_style)
        ])

    # Construcción de la tabla
    tabla = Table(data, colWidths=[40, 240, 260])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#002B49')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))

    story.append(tabla)
    doc.build(story)
    return response


# ==========================================
# EXPORTAR A EXCEL
# ==========================================
def maquina_exportar_excel(request):
    query = request.GET.get('q', '').strip()
    institucion_id = request.GET.get('institucion_id', '').strip()

    maquinas = Maquina.objects.all().select_related('institucion')

    if query:
        maquinas = maquinas.filter(
            Q(serie_dispositivo__icontains=query) | 
            Q(institucion__nombre__icontains=query)
        )

    if institucion_id:
        maquinas = maquinas.filter(institucion_id=institucion_id)

    # Crear libro openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Máquinas"

    # Estilos OpenPyXL
    font_titulo = Font(name='Calibri', size=14, bold=True, color='002B49')
    font_header = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
    fill_header = PatternFill(start_color='002B49', end_color='002B49', fill_type='solid')
    border_thin = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )
    align_center = Alignment(horizontal='center', vertical='center')
    align_left = Alignment(horizontal='left', vertical='center')

    # Título
    ws.merge_cells('A1:C1')
    ws['A1'] = "REPORTE DE MÁQUINAS Y DISPOSITIVOS"
    ws['A1'].font = font_titulo
    ws['A1'].alignment = align_center

    # Cabeceras
    headers = ["ID", "Serie Dispositivo", "Institución Educativa"]
    ws.append([])  # Fila 2 en blanco
    ws.append(headers)  # Fila 3 cabecera

    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_num)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = border_thin

    # Datos
    for m in maquinas:
        row = [
            m.id,
            m.serie_dispositivo,
            m.institucion.nombre if m.institucion else "-"
        ]
        ws.append(row)
        current_row = ws.max_row
        
        ws.cell(row=current_row, column=1).alignment = align_center
        ws.cell(row=current_row, column=2).alignment = align_left
        ws.cell(row=current_row, column=3).alignment = align_left

        for col_num in range(1, 4):
            ws.cell(row=current_row, column=col_num).border = border_thin

    # Anchos de columna automáticos
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 38
    ws.column_dimensions['C'].width = 45

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="reporte_maquinas.xlsx"'
    wb.save(response)
    return response
