from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from asistencia.models import Personal, Asistencia

class Command(BaseCommand):
    help = 'Genera automáticamente las plantillas de asistencia diaria para el personal activo'

    def add_arguments(self, parser):
        # Permite pasar una fecha manual por consola: --fecha 2026-10-28
        parser.add_argument(
            '--fecha',
            type=str,
            help='Fecha simulada en formato YYYY-MM-DD para pruebas',
        )

    def handle(self, *args, **options):
        # Si se pasa una fecha por parámetro, la usamos; si no, usamos la fecha local actual de Lima
        fecha_str = options.get('fecha')
        if fecha_str:
            try:
                hoy_lima = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                self.stdout.write(self.style.MIGRATE_LABEL(f"=== MODO SIMULACIÓN: Probando con la fecha {hoy_lima} ==="))
            except ValueError:
                self.stdout.write(self.style.ERROR("Formato de fecha inválido. Use YYYY-MM-DD."))
                return
        else:
            hoy_lima = timezone.localdate() 
        
        # 1. Validar que sea de Lunes a Viernes (0=Lunes, 4=Viernes)
        if hoy_lima.weekday() > 4:
            self.stdout.write(self.style.WARNING(f"La fecha {hoy_lima} es fin de semana. No se generan asistencias."))
            return

        # 2. Mapear días con consistencia de mayúsculas
        dias_map = {
            0: 'LUNES', 
            1: 'MARTES', 
            2: 'MIERCOLES', 
            3: 'JUEVES', 
            4: 'VIERNES'
        }
        dia_actual_texto = dias_map[hoy_lima.weekday()]

        # Filtrar personal activo cuyo día de descanso NO sea hoy
        personal_activo = Personal.objects.filter(
            condicion=True
        ).exclude(
            dia_descanso__iexact=dia_actual_texto
        )

        if not personal_activo.exists():
            self.stdout.write(self.style.WARNING(f"No se encontró personal activo asignado para laborar el día ({dia_actual_texto})."))
            return

        asistencias_a_crear = []

        # 3. Preparar inserciones masivas evitando duplicados
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

        # Inserción optimizada en un solo query
        if asistencias_a_crear:
            Asistencia.objects.bulk_create(asistencias_a_crear)
            registros_creados = len(asistencias_a_crear)
            self.stdout.write(self.style.SUCCESS(
                f"Se crearon exitosamente {registros_creados} registros de asistencia para el día: {hoy_lima}."
            ))
        else:
            self.stdout.write(self.style.WARNING(f"Las plantillas de asistencia para el día {hoy_lima} ya estaban creadas."))
