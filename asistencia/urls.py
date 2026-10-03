#from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
     
    path('', views.inicio_index, name='inicio'),

    path('ugel/', views.ugel_mantenimiento, name='ugel_mantenimiento'),
    #Cargos
    path('cargos/', views.cargo_listar, name='cargo_listar'),
    path('cargos/crear/', views.cargo_crear, name='cargo_crear'),
    path('cargos/editar/<int:pk>/', views.cargo_editar, name='cargo_editar'),
    path('cargos/anular/<int:pk>/', views.cargo_anular, name='cargo_anular'),
    path('cargos/pdf/', views.cargo_reporte_pdf, name='cargo_pdf'),
    path('cargos/excel/', views.cargo_exportar_excel, name='cargo_excel'),
    #Niveles
    path('niveles/', views.nivel_listar, name='nivel_listar'),
    path('niveles/crear/', views.nivel_crear, name='nivel_crear'),
    path('niveles/editar/<int:pk>/', views.nivel_editar, name='nivel_editar'),
    path('niveles/anular/<int:pk>/', views.nivel_anular, name='nivel_anular'),
    path('niveles/pdf/', views.nivel_reporte_pdf, name='nivel_pdf'),
    path('niveles/excel/', views.nivel_exportar_excel, name='nivel_excel'),
    # Turnos
    path('turnos/', views.turno_listar, name='turno_listar'),
    path('turnos/crear/', views.turno_crear, name='turno_crear'),
    path('turnos/editar/<int:pk>/', views.turno_editar, name='turno_editar'),
    path('turnos/anular/<int:pk>/', views.turno_anular, name='turno_anular'),
    path('turnos/pdf/', views.turno_reporte_pdf, name='turno_pdf'),
    path('turnos/excel/', views.turno_exportar_excel, name='turno_excel'),

    # Distritos
    path('distritos/', views.distrito_listar, name='distrito_listar'),
    path('distritos/crear/', views.distrito_crear, name='distrito_crear'),
    path('distritos/editar/<int:pk>/', views.distrito_editar, name='distrito_editar'),
    path('distritos/anular/<int:pk>/', views.distrito_anular, name='distrito_anular'),
    path('distritos/pdf/', views.distrito_reporte_pdf, name='distrito_pdf'),
    path('distritos/excel/', views.distrito_exportar_excel, name='distrito_excel'),

    # Faltas
    path('faltas/', views.falta_listar, name='falta_listar'),
    path('faltas/crear/', views.falta_crear, name='falta_crear'),
    path('faltas/editar/<int:pk>/', views.falta_editar, name='falta_editar'),
    path('faltas/anular/<int:pk>/', views.falta_anular, name='falta_anular'),
    path('faltas/pdf/', views.falta_reporte_pdf, name='falta_pdf'),
    path('faltas/excel/', views.falta_exportar_excel, name='falta_excel'),

    # Tardanzas
    path('tardanzas/', views.tardanza_listar, name='tardanza_listar'),
    path('tardanzas/crear/', views.tardanza_crear, name='tardanza_crear'),
    path('tardanzas/editar/<int:pk>/', views.tardanza_editar, name='tardanza_editar'),
    path('tardanzas/anular/<int:pk>/', views.tardanza_anular, name='tardanza_anular'),
    path('tardanzas/pdf/', views.tardanza_reporte_pdf, name='tardanza_pdf'),
    path('tardanzas/excel/', views.tardanza_exportar_excel, name='tardanza_excel'),

    # Instituciones
    path('instituciones/', views.institucion_listar, name='institucion_listar'),
    path('instituciones/crear/', views.institucion_crear, name='institucion_crear'),
    path('instituciones/editar/<int:pk>/', views.institucion_editar, name='institucion_editar'),
    path('instituciones/anular/<int:pk>/', views.institucion_anular, name='institucion_anular'),
    path('instituciones/pdf/', views.institucion_reporte_pdf, name='institucion_pdf'),
    path('instituciones/excel/', views.institucion_exportar_excel, name='institucion_excel'),

    # En asistencia/urls.py
    path('instituciones/validar-codigo/', views.verificar_codigo_modular, name='verificar_codigo_modular'),

    # Personal
    path('personal/', views.personal_listar, name='personal_listar'),
    path('personal/crear/', views.personal_crear, name='personal_crear'),
    path('personal/editar/<int:pk>/', views.personal_editar, name='personal_editar'),
    path('personal/anular/<int:pk>/', views.personal_anular, name='personal_anular'),
    path('personal/pdf/', views.personal_reporte_pdf, name='personal_pdf'),
    path('personal/excel/', views.personal_exportar_excel, name='personal_excel'),
    path('personal/validar/', views.verificar_unicidad_personal, name='verificar_unicidad_personal'),

    path('maquinas/', views.maquina_listar, name='maquina_listar'),
    path('maquinas/crear/', views.maquina_crear, name='maquina_crear'),
    path('maquinas/editar/<int:pk>/', views.maquina_editar, name='maquina_editar'),
    path('maquinas/eliminar/<int:pk>/', views.maquina_eliminar, name='maquina_eliminar'),
    path('maquinas/verificar-unicidad/', views.verificar_unicidad_maquina, name='verificar_unicidad_maquina'),
    
    path('nosotros/', views.nosotros, name='nosotros'),
]
