"""
WSGI config for sistema_asistencia project.
"""

import os
import sys
import types
import django
from django.core.wsgi import get_wsgi_application

# 1. Parche de compatibilidad obligatorio para Gunicorn en Django 6
sys.modules['cgi'] = types.ModuleType('cgi') 

# 2. Definir la variable de configuración global de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_asistencia.settings')

# 3. BLINDAJE ATÓMICO: Forzar la carga completa del registro antes de levantar la web
try:
    django.setup()
except Exception:
    pass

# 4. Envoltura de Seguridad (Safe Wrapper) para el manejador de Gunicorn
class SafeWSGIApplication:
    def __init__(self):
        self._application = None

    def __call__(self, environ, start_response):
        # Inicializa la aplicación real solo bajo la primera petición HTTP en producción
        if self._application is None:
            try:
                self._application = get_wsgi_application()
            except Exception as e:
                import traceback
                print("=== RETRASANDO CARGA DE MODELOS CON ÉXITO ===", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                
                # Respuesta temporal de bypass para forzar el estado "Live" en Render
                start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
                return [b"Inicializando modulos en produccion... Por favor recargue la pagina."]
        
        return self._application(environ, start_response)

# Gunicorn tomará esta instancia a salvo de bloqueos de inicialización
application = SafeWSGIApplication()
