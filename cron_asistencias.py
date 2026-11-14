import os
import sys
import django
from datetime import datetime

# Inicialización autónoma del entorno Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_asistencia.settings")
django.setup()

# Importaciones del ORM de Django
from django.utils import timezone
from asistencia.models import Personal, Asistencia


def ejecutar_generacion(fecha_manual=None):
    if fecha_manual:
        try:
            hoy_lima = datetime.strptime(fecha_manual, "%Y-%m-%d").date()
            print(f"=== MODO SIMULACIÓN: Ejecutando con fecha {hoy_lima} ===")
        except ValueError:
            print("Error: Formato de fecha inválido. Use el formato YYYY-MM-DD.")
            return
    else:
        # Obtener la fecha exacta basada en la zona horaria local de Lima (Evita desfases UTC)
        ahora_lima = timezone.localtime(timezone.now())
        hoy_lima = ahora_lima.date()

    # 1. Obtener todo el personal activo en el sistema
    personal_activo = Personal.objects.filter(condicion=True)
    if not personal_activo.exists():
        print("No se encontró personal activo asignado en el sistema.")
        return

    asistencias_a_crear = []

    # 2. Preparar inserciones masivas evitando duplicados para el mismo día
    for empleado in personal_activo:
        asistencia_existe = Asistencia.objects.filter(
            personal=empleado, fecha=hoy_lima
        ).exists()

        if not asistencia_existe:
            asistencias_a_crear.append(
                Asistencia(
                    personal=empleado,
                    fecha=hoy_lima,
                    h_entrada=None,
                    h_salida=None,
                    justificado=False,
                )
            )

    # 3. Inserción atómica masiva en un solo query mediante el ORM
    if asistencias_a_crear:
        Asistencia.objects.bulk_create(asistencias_a_crear)
        print(
            f"Éxito: Se crearon {len(asistencias_a_crear)} plantillas de asistencia libres para el día: {hoy_lima}."
        )
    else:
        print(
            f"Aviso: Las plantillas de asistencia para el día {hoy_lima} ya se encuentran registradas."
        )


if __name__ == "__main__":
    # Captura el argumento de fecha opcional pasado por consola (ej. 2026-10-28)
    argumento_fecha = sys.argv[1] if len(sys.argv) > 1 else None
    ejecutar_generacion(argumento_fecha)
