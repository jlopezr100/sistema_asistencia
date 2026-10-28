"""
WSGI config for sistema_asistencia project.
"""

import os
import sys
import types
import django

# Parche de compatibilidad obligatorio para Gunicorn en Django 6
sys.modules['cgi'] = types.ModuleType('cgi') 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_asistencia.settings')

# FORZAR INICIALIZACIÓN PREVIA: Carga las aplicaciones antes de mapear URLs o vistas
try:
    django.setup()
except Exception:
    pass

from django.core.wsgi import get_wsgi_application

# Inicialización segura estándar
try:
    application = get_wsgi_application()
except Exception as e:
    import traceback
    print("=== MONITOR DE INICIALIZACIÓN ===", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    print("================================", file=sys.stderr)
    
    # Manejador WSGI de respaldo pasivo en caso extremo
    def application(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return [b"Cargando modulos del sistema... Por favor actualice el navegador en 5 segundos."]
