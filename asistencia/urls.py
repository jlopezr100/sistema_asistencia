from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
     path('admin/', admin.site.urls),
     
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
    
    path('nosotros/', views.nosotros, name='nosotros'),

]