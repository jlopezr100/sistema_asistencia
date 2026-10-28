from django.utils import timezone
from datetime import datetime

def procesar_plantillas_asistencia(command_instance, fecha_str=None):
    # Los modelos se importan de forma segura aquí, totalmente fuera del ciclo de carga de comandos
    from asistencia.models import Personal, Asistencia

    if fecha_str:
        try:
            hoy_lima = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            command_instance.stdout.write(command_instance.style.MIGRATE_LABEL(f"=== MODO SIMULACIÓN: Probando con la fecha {hoy_lima} ==="))
        except ValueError:
            command_instance.stdout.write(command_instance.style.ERROR("Formato de fecha inválido. Use YYYY-MM-DD."))
            return
    else:
        hoy_lima = timezone.localdate() 
    
    # 1. Validar Lunes a Viernes
    if hoy_lima.weekday() > 4:
        command_instance.stdout.write(command_instance.style.WARNING(f"La fecha {hoy_lima} es fin de semana. No se generan asistencias."))
        return

    # 2. Mapear días
    dias_map = {0: 'LUNES', 1: 'MARTES', 2: 'MIERCOLES', 3: 'JUEVES', 4: 'VIERNES'}
    dia_actual_texto = dias_map[hoy_lima.weekday()]

    personal_activo = Personal.objects.filter(
        condicion=True
    ).exclude(
        dia_descanso__iexact=dia_actual_texto
    )

    if not personal_activo.exists():
        command_instance.stdout.write(command_instance.style.WARNING(f"No se encontró personal activo asignado para laborar el día ({dia_actual_texto})."))
        return

    asistencias_a_crear = []

    # 3. Preparar inserciones masivas
    for empleado in personal_activo:
        asistencia_existe = Asistencia.objects.filter(
            personal=empleado, 
            fecha=hoy_lima
        ).exists()
        
        if not asistencia_existe:
            asistencias_a_crear.append(
                Asistencia(
                    personal=empleado,
                    fecha=hoy_lima,
                    h_entrada=None,
                    h_salida=None,
                    justificado=False
                )
            )

    if asistencias_a_crear:
        Asistencia.objects.bulk_create(asistencias_a_crear)
        registros_creados = len(asistencias_a_crear)
        command_instance.stdout.write(command_instance.style.SUCCESS(
            f"Se crearon exitosamente {registros_creados} registros de asistencia para el día: {hoy_lima}."
        ))
    else:
        command_instance.stdout.write(command_instance.style.WARNING(f"Las plantillas de asistencia para el día {hoy_lima} ya estaban creadas."))
