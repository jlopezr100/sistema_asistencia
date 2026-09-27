"""
Django settings for sistema_asistencia project.
Optimized and Cleaned for Production Deployment.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# 1. Directorio Base y Carga de Entorno
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 2. Configuración de Seguridad Crítica
SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key-default')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# 3. Aplicaciones Instaladas (Estructura Unificada)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',         # <-- Almacenamiento en la nube antes de staticfiles
    'django.contrib.staticfiles',
    'cloudinary',                 # <-- Aplicación Cloudinary
    'asistencia',                 # <-- Tu aplicación local
]

# 4. Middleware (WhiteNoise integrado para estilos estáticos)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sistema_asistencia.urls'

# 5. Motor de Plantillas (¡Restaurado el Procesador de Contexto de la UGEL!)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'asistencia.context_processors.ugel_context', # <-- CRUCIAL PARA MOSTRAR LOS DATOS DE LA UGEL
            ],
        },
    },
]

WSGI_APPLICATION = 'sistema_asistencia.wsgi.application'

# 6. Base de Datos Enlazada con Parche SSL para Aiven
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

if not DEBUG and DATABASES['default'].get('ENGINE') == 'django.db.backends.mysql':
    DATABASES['default']['OPTIONS'] = {
        'ssl': {
            'ssl_mode': 'REQUIRED'
        }
    }

# 7. Validadores de Contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 8. Servidor de Almacenamiento Cloudinary para Imágenes Multimedia
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudStorage'

# 9. Manejo de Archivos Estáticos (CSS, JS)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# 10. Manejo de Archivos de Medios locales (Básicos)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 11. Internacionalización e Idioma
LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True
