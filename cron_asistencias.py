import os
import sys
import django
from datetime import datetime
from zoneinfo import ZoneInfo

# Inicialización autónoma del entorno Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_asistencia.settings")
django.setup()

# Importaciones del ORM de Django
from django.utils import timezone
from asistencia.models import Personal, Asistencia


def ejecutar_generacion(fecha_manual=None):
    zona_lima = ZoneInfo("America/Lima")

    if fecha_manual:
        try:
            hoy_lima = datetime.strptime(fecha_manual, "%Y-%m-%d").date()
            print(f"=== MODO SIMULACIÓN: Ejecutando con fecha {hoy_lima} ===")
        except ValueError:
            print("Error: Formato de fecha inválido. Use el formato YYYY-MM-DD.")
            return
    else:
        # Obtener la fecha exacta en Lima, Perú (evita desfases UTC de Render/Aiven)
        ahora_lima = timezone.now().astimezone(zona_lima)
        hoy_lima = ahora_lima.date()
        print(f"=== EJECUCIÓN AUTOMÁTICA (Hora Lima: {ahora_lima.strftime('%Y-%m-%d %H:%M:%S')}) ===")

    # 1. Obtener todo el personal activo en el sistema
    personal_activo = Personal.objects.filter(condicion=True)
    if not personal_activo.exists():
        print("No se encontró personal activo asignado en el sistema.")
        return

    # 2. Obtener en una sola consulta los IDs del personal que YA tiene registro hoy (más rápido y eficiente)
    ids_registrados = set(
        Asistencia.objects.filter(fecha=hoy_lima).values_list("personal_id", flat=True)
    )

    asistencias_a_crear = []

    # 3. Preparar inserciones masivas solo para quienes aún no tienen plantilla hoy
    for empleado in personal_activo:
        if empleado.id not in ids_registrados:
            asistencias_a_crear.append(
                Asistencia(
                    personal=empleado,
                    fecha=hoy_lima,
                    h_entrada=None,
                    h_salida=None,
                    justificado=False,
                )
            )

    # 4. Inserción atómica masiva en un solo query mediante el ORM
    if asistencias_a_crear:
        Asistencia.objects.bulk_create(asistencias_a_crear)
        print(
            f"Éxito: Se crearon {len(asistencias_a_crear)} plantillas de asistencia para el día: {hoy_lima}."
        )
    else:
        print(
            f"Aviso: Las plantillas de asistencia para el día {hoy_lima} ya se encuentran registradas."
        )


if __name__ == "__main__":
    # Captura el argumento de fecha opcional pasado por consola (ej. python cron_asistencias.py 2026-11-18)
    argumento_fecha = sys.argv[1] if len(sys.argv) > 1 else None
    ejecutar_generacion(argumento_fecha)
