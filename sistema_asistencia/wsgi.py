import os
import sys
import types
from django.core.wsgi import get_wsgi_application

sys.modules['cgi'] = types.ModuleType('cgi') 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_asistencia.settings')
application = get_wsgi_application()
