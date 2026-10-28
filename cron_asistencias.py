import os
import sys
import django
from datetime import datetime

# Inicialización autónoma del entorno Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_asistencia.settings')
django.setup()

# Importaciones diferidas seguras del ORM
from django.utils import timezone
from asistencia.models import Personal, Asistencia, Corte

def ejecutar_generacion(fecha_manual=None):
    if fecha_manual:
        try:
            hoy_lima = datetime.strptime(fecha_manual, '%Y-%m-%d').date()
            print(f"=== MODO SIMULACIÓN: Ejecutando con fecha {hoy_lima} ===")
        except ValueError:
            print("Error: Formato de fecha inválido. Use YYYY-MM-DD.")
            return
    else:
        hoy_lima = timezone.localdate() 
    
    # 1. Validar que sea de Lunes a Viernes (0=Lunes, 4=Viernes)
    if hoy_lima.weekday() > 4:
        print(f"La fecha {hoy_lima} es fin de semana. No se generan asistencias.")
        return

    # 2. Mapear días de la semana
    dias_map = {0: 'LUNES', 1: 'MARTES', 2: 'MIERCOLES', 3: 'JUEVES', 4: 'VIERNES'}
    dia_actual_texto = dias_map[hoy_lima.weekday()]

    # Filtrar personal activo cuyo día de descanso NO sea hoy
    personal_activo = Personal.objects.filter(
        condicion=True
    ).exclude(
        dia_descanso__iexact=dia_actual_texto
    )

    if not personal_activo.exists():
        print(f"No se encontró personal activo asignado para trabajar el día ({dia_actual_texto}).")
        return

    # 3. Buscar periodo de corte activo para hoy
    corte_actual = Corte.objects.filter(f_inicio__lte=hoy_lima, f_final__gte=hoy_lima, procesado=False).first()

    asistencias_a_crear = []

    # 4. Preparar inserciones masivas evitando duplicados de llave primaria
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
                    justificado=False,
                    corte=corte_actual
                )
            )

    # Inserción atómica masiva en un solo query
    if asistencias_a_crear:
        Asistencia.objects.bulk_create(asistencias_a_crear)
        print(f"Éxito: Se crearon {len(asistencias_a_crear)} plantillas de asistencia para el día: {hoy_lima}.")
    else:
        print(f"Aviso: Las plantillas de asistencia para el día {hoy_lima} ya estaban registradas.")

if __name__ == '__main__':
    # Permite inyectar parámetros por consola: python cron_asistencias.py 2026-10-28
    argumento_fecha = sys.argv[1] if len(sys.argv) > 1 else None
    ejecutar_generacion(argumento_fecha)

