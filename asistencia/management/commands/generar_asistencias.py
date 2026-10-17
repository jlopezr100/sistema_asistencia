from django.core.management.base import BaseCommand
from datetime import date
from asistencia.models import Personal, Asistencia

class Command(BaseCommand):
    help = 'Genera automáticamente las plantillas de asistencia diaria a las 00:00 para el personal activo'

    def handle(self, *args, **options):
        hoy = date.today()
        
        # 1. Validar que sea de Lunes a Viernes (0=Lunes, 4=Viernes)
        if hoy.weekday() > 4:
            self.stdout.write(self.style.WARNING("Hoy es fin de semana. No se generan asistencias."))
            return

        # 2. Filtrar personal activo cuyo día de descanso NO sea hoy
        dias_map = {0: 'LUNES', 1: 'MARTES', 2: 'MIERCOLES', 3: 'JUEVES', 4: 'VIERNES'}
        dia_actual_texto = dias_map[hoy.weekday()]
        
        personal_activo = Personal.objects.filter(
            condicion=True
        ).exclude(
            dia_descanso=dia_actual_texto
        )

        registros_creados = 0

        # 3. Crear el registro en la tabla Asistencia de forma libre (Corte nacerá en NULL)
        for empleado in personal_activo:
            asistencia_existe = Asistencia.objects.filter(personal=empleado, fecha=hoy).exists()
            
            if not asistencia_existe:
                Asistencia.objects.create(
                    personal=empleado,
                    h_entrada=None,
                    h_salida=None,
                    justificado=False
                )
                registros_creados += 1

        self.stdout.write(self.style.SUCCESS(f"Se crearon exitosamente {registros_creados} registros de asistencia para el día de hoy."))
