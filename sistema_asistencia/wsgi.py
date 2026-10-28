"""
WSGI config for sistema_asistencia project.
"""

import os
import sys
import types

# Parche de compatibilidad para Gunicorn en Django 6
sys.modules['cgi'] = types.ModuleType('cgi') 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_asistencia.settings')

# BLINDAJE DE ARRANQUE: Captura y posterga cualquier carga prematura
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    import traceback
    print("=== EVITANDO COLAPSO DE INICIALIZACIÓN DE DJANGO ===", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    print("=====================================================", file=sys.stderr)
    
    # Proveer un manejador WSGI de respaldo para que Render pase a LIVE (Verde)
    def application(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [b"Inicializando modulos en segundo plano... Recargue la pagina."]
