from django.urls import path
from django.utils.module_loading import import_string

# Función auxiliar para instanciar vistas bajo demanda (Lazy Loading)
def lazy_view(view_path):
    def wrapper(request, *args, **kwargs):
        view_func = import_string(view_path)
        return view_func(request, *args, **kwargs)
    return wrapper

urlpatterns = [
    path('', lazy_view('asistencia.views.inicio_views.inicio_index'), name='inicio'),
    path('ugel/', lazy_view('asistencia.views.ugel_views.ugel_mantenimiento'), name='ugel_mantenimiento'),
    
    # Mantenimiento de Cargos
    path('cargos/', lazy_view('asistencia.views.cargo_views.cargo_listar'), name='cargo_listar'),
    path('cargos/crear/', lazy_view('asistencia.views.cargo_views.cargo_crear'), name='cargo_crear'),
    path('cargos/editar/<int:pk>/', lazy_view('asistencia.views.cargo_views.cargo_editar'), name='cargo_editar'),
    path('cargos/anular/<int:pk>/', lazy_view('asistencia.views.cargo_views.cargo_anular'), name='cargo_anular'),
    path('cargos/pdf/', lazy_view('asistencia.views.cargo_views.cargo_reporte_pdf'), name='cargo_pdf'),
    path('cargos/excel/', lazy_view('asistencia.views.cargo_views.cargo_exportar_excel'), name='cargo_excel'),
    
    # Mantenimiento de Niveles
    path('niveles/', lazy_view('asistencia.views.nivel_views.nivel_listar'), name='nivel_listar'),
    path('niveles/crear/', lazy_view('asistencia.views.nivel_views.nivel_crear'), name='nivel_crear'),
    path('niveles/editar/<int:pk>/', lazy_view('asistencia.views.nivel_views.nivel_editar'), name='nivel_editar'),
    path('niveles/anular/<int:pk>/', lazy_view('asistencia.views.nivel_views.nivel_anular'), name='nivel_anular'),
    path('niveles/pdf/', lazy_view('asistencia.views.nivel_views.nivel_reporte_pdf'), name='nivel_pdf'),
    path('niveles/excel/', lazy_view('asistencia.views.nivel_views.nivel_exportar_excel'), name='nivel_excel'),
    
    # Mantenimiento de Turnos
    path('turnos/', lazy_view('asistencia.views.turno_views.turno_listar'), name='turno_listar'),
    path('turnos/crear/', lazy_view('asistencia.views.turno_views.turno_crear'), name='turno_crear'),
    path('turnos/editar/<int:pk>/', lazy_view('asistencia.views.turno_views.turno_editar'), name='turno_editar'),
    path('turnos/anular/<int:pk>/', lazy_view('asistencia.views.turno_views.turno_anular'), name='turno_anular'),
    path('turnos/pdf/', lazy_view('asistencia.views.turno_views.turno_reporte_pdf'), name='turno_pdf'),
    path('turnos/excel/', lazy_view('asistencia.views.turno_views.turno_exportar_excel'), name='turno_excel'),

    # Mantenimiento de Distritos
    path('distritos/', lazy_view('asistencia.views.distrito_views.distrito_listar'), name='distrito_listar'),
    path('distritos/crear/', lazy_view('asistencia.views.distrito_crear'), name='distrito_crear'),
    path('distritos/editar/<int:pk>/', lazy_view('asistencia.views.distrito_views.distrito_editar'), name='distrito_editar'),
    path('distritos/anular/<int:pk>/', lazy_view('asistencia.views.distrito_views.distrito_anular'), name='distrito_anular'),
    path('distritos/pdf/', lazy_view('asistencia.views.distrito_views.distrito_reporte_pdf'), name='distrito_pdf'),
    path('distritos/excel/', lazy_view('asistencia.views.distrito_views.distrito_exportar_excel'), name='distrito_excel'),

    # Control de Faltas
    path('faltas/', lazy_view('asistencia.views.falta_views.falta_listar'), name='falta_listar'),
    path('faltas/crear/', lazy_view('asistencia.views.falta_views.falta_crear'), name='falta_crear'),
    path('faltas/editar/<int:pk>/', lazy_view('asistencia.views.falta_views.falta_editar'), name='falta_editar'),
    path('faltas/anular/<int:pk>/', lazy_view('asistencia.views.falta_views.falta_anular'), name='falta_anular'),
    path('faltas/pdf/', lazy_view('asistencia.views.falta_views.falta_reporte_pdf'), name='falta_pdf'),
    path('faltas/excel/', lazy_view('asistencia.views.falta_views.falta_exportar_excel'), name='falta_excel'),

    # Control de Tardanzas
    path('tardanzas/', lazy_view('asistencia.views.tardanza_views.tardanza_listar'), name='tardanza_listar'),
    path('tardanzas/crear/', lazy_view('asistencia.views.tardanza_views.tardanza_crear'), name='tardanza_crear'),
    path('tardanzas/editar/<int:pk>/', lazy_view('asistencia.views.tardanza_views.tardanza_editar'), name='tardanza_editar'),
    path('tardanzas/anular/<int:pk>/', lazy_view('asistencia.views.tardanza_views.tardanza_anular'), name='tardanza_anular'),
    path('tardanzas/pdf/', lazy_view('asistencia.views.tardanza_views.tardanza_reporte_pdf'), name='tardanza_pdf'),
    path('tardanzas/excel/', lazy_view('asistencia.views.tardanza_views.tardanza_exportar_excel'), name='tardanza_excel'),

    # Instituciones Educativas
    path('instituciones/', lazy_view('asistencia.views.instituciones_views.institucion_listar'), name='institucion_listar'),
    path('instituciones/crear/', lazy_view('asistencia.views.instituciones_views.institucion_crear'), name='institucion_crear'),
    path('instituciones/editar/<int:pk>/', lazy_view('asistencia.views.instituciones_views.institucion_editar'), name='institucion_editar'),
    path('instituciones/anular/<int:pk>/', lazy_view('asistencia.views.instituciones_views.institucion_anular'), name='institucion_anular'),
    path('instituciones/pdf/', lazy_view('asistencia.views.instituciones_views.institucion_reporte_pdf'), name='institucion_pdf'),
    path('instituciones/excel/', lazy_view('asistencia.views.instituciones_views.institucion_exportar_excel'), name='institucion_excel'),
    path('instituciones/validar-codigo/', lazy_view('asistencia.views.instituciones_views.verificar_codigo_modular'), name='verificar_codigo_modular'),

    # Gestión de Personal
    path('personal/', lazy_view('asistencia.views.personal_views.personal_listar'), name='personal_listar'),
    path('personal/crear/', lazy_view('asistencia.views.personal_views.personal_crear'), name='personal_crear'),
    path('personal/editar/<int:pk>/', lazy_view('asistencia.views.personal_views.personal_editar'), name='personal_editar'),
    path('personal/anular/<int:pk>/', lazy_view('asistencia.views.personal_views.personal_anular'), name='personal_anular'),
    path('personal/pdf/', lazy_view('asistencia.views.personal_views.personal_reporte_pdf'), name='personal_pdf'),
    path('personal/excel/', lazy_view('asistencia.views.personal_views.personal_exportar_excel'), name='personal_excel'),
    path('personal/validar/', lazy_view('asistencia.views.personal_views.verificar_unicidad_personal'), name='verificar_unicidad_personal'),

    # Dispositivos Quioscos (Máquinas)
    path('maquinas/', lazy_view('asistencia.views.maquinas_views.maquina_listar'), name='maquina_listar'),
    path('maquinas/crear/', lazy_view('asistencia.views.maquinas_views.maquina_crear'), name='maquina_crear'),
    path('maquinas/editar/<int:pk>/', lazy_view('asistencia.views.maquinas_views.maquina_editar'), name='maquina_editar'),
    path('maquinas/eliminar/<int:pk>/', lazy_view('asistencia.views.maquinas_views.maquina_eliminar'), name='maquina_eliminar'),
    path('maquinas/verificar-unicidad/', lazy_view('asistencia.views.maquinas_views.verificar_unicidad_maquina'), name='verificar_unicidad_maquina'),
    path('maquinas/exportar/pdf/', lazy_view('asistencia.views.maquinas_views.maquina_exportar_pdf'), name='maquina_exportar_pdf'),
    path('maquinas/exportar/excel/', lazy_view('asistencia.views.maquinas_views.maquina_exportar_excel'), name='maquina_exportar_excel'),

    # endpoints del Módulo de Marcado Biométrico
    path('asistencia/marcar/', lazy_view('asistencia.views.asistencia_views.mostrar_pantalla_marcado'), name='mostrar_marcado'),
    path('asistencia/api/registrar/', lazy_view('asistencia.views.asistencia_views.registrar_marcado_tiempo_real'), name='api_registrar_marcado'),

    path('nosotros/', lazy_view('asistencia.views.nosotros_views.nosotros'), name='nototros'),
]
