from django.core.management.base import BaseCommand
from datetime import date
import datetime
from asistencia.models import Personal, Asistencia, Corte

class Command(BaseCommand):
    help = 'Genera automáticamente las plantillas de asistencia diaria a las 00:00 para el personal activo'

    def handle(self, *args, **options):
        hoy = date.today()
        
        # 1. Validar que sea de Lunes a Viernes (0=Lunes, 4=Viernes, 5=Sábado, 6=Domingo)
        if hoy.weekday() > 4:
            self.stdout.write(self.style.WARNING("Hoy es fin de semana. No se generan asistencias."))
            return

        # 2. Buscar el Periodo de Corte activo para la fecha de hoy
        corte_actual = Corte.objects.filter(f_inicio__lte=hoy, f_final__gte=hoy, procesado=False).first()
        if not corte_actual:
            self.stdout.write(self.style.ERROR("Error: No existe un Periodo de Corte activo para la fecha de hoy."))
            return

        # 3. Filtrar personal activo cuyo día de descanso NO sea hoy
        # Transformamos el número de día a texto para comparar con tu campo 'dia_descanso'
        dias_map = {0: 'LUNES', 1: 'MARTES', 2: 'MIERCOLES', 3: 'JUEVES', 4: 'VIERNES'}
        dia_actual_texto = dias_map[hoy.weekday()]
        
        personal_activo = Personal.objects.filter(
            condicion=True
        ).exclude(
            dia_descanso=dia_actual_texto
        )

        registros_creados = 0

        # 4. Crear el registro en la tabla Asistencia si no existe ya
        for empleado in personal_activo:
            # Evita duplicados si el comando se corre dos veces por error
            asistencia_existe = Asistencia.objects.filter(personal=empleado, fecha=hoy).exists()
            
            if not asistencia_existe:
                Asistencia.objects.create(
                    personal=empleado,
                    corte=corte_actual,
                    # Dejamos h_entrada y h_salida en None/Null, se llenarán cuando marquen su huella
                    h_entrada=None,
                    h_salida=None,
                    justificado=False
                )
                registros_creados += 1

        self.stdout.write(self.style.SUCCESS(f"Se crearon exitosamente {registros_creados} registros de asistencia para el día de hoy."))
