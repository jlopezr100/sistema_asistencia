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

# PASO CLAVE: Forzar a Django a cargar el registro de apps antes de compilar las vistas
django.setup()

from django.core.wsgi import get_wsgi_application

# Dejar que get_wsgi_application cargue el enrutador de forma nativa
application = get_wsgi_application()
