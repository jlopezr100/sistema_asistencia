from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Genera automáticamente las plantillas de asistencia diaria para el personal activo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fecha',
            type=str,
            help='Fecha simulada en formato YYYY-MM-DD para pruebas',
        )

    def handle(self, *args, **options):
        # Importación tardía estricta para no interferir en el ciclo de compilación
        from asistencia.services import procesar_plantillas_asistencia
        
        fecha_str = options.get('fecha')
        procesar_plantillas_asistencia(self, fecha_str)
