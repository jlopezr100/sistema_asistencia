"""
WSGI config for sistema_asistencia project.
"""

import os
import sys
import types
from django.core.wsgi import get_wsgi_application

# Parche de compatibilidad obligatorio para Gunicorn en Django 6
sys.modules['cgi'] = types.ModuleType('cgi') 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_asistencia.settings')

# Dejar que Django tome el control total del manejo y renderizado de excepciones en pantalla
application = get_wsgi_application()
