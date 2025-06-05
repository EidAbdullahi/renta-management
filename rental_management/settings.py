import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url


# Cloudinary
import cloudinary
import cloudinary.uploader
import cloudinary.api


# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent


# SECRET KEY
SECRET_KEY = config('SECRET_KEY')


# DEBUG MODE
DEBUG = config('DEBUG', cast=bool)


# ALLOWED HOSTS
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# APPLICATIONS
INSTALLED_APPS = [
   'django.contrib.admin',
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.messages',
   'django.contrib.staticfiles',
   'django.contrib.humanize',

   # Your apps
   'users',
   'freelancers',
   'offplan',

   # Third-party
   'widget_tweaks',
   'cloudinary',
   'cloudinary_storage',
]


# MIDDLEWARE
MIDDLEWARE = [
   'django.middleware.security.SecurityMiddleware',
   'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
   'django.contrib.sessions.middleware.SessionMiddleware',
   'django.middleware.common.CommonMiddleware',
   'django.middleware.csrf.CsrfViewMiddleware',
   'django.contrib.auth.middleware.AuthenticationMiddleware',
   'django.contrib.messages.middleware.MessageMiddleware',
   'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ROOT URL
ROOT_URLCONF = 'rental_management.urls'


# TEMPLATE CONFIG
TEMPLATES = [
   {
       'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'DIRS': [
           BASE_DIR / 'templates',
           BASE_DIR / 'users/templates',
           BASE_DIR / 'freelancers/templates',
       ],
       'APP_DIRS': True,
       'OPTIONS': {
           'context_processors': [
               'django.template.context_processors.debug',
               'django.template.context_processors.request',
               'django.contrib.auth.context_processors.auth',
               'django.contrib.messages.context_processors.messages',
           ],
       },
   },
]


# WSGI
WSGI_APPLICATION = 'rental_management.wsgi.application'




# DATABASES
DATABASES = {
   'default': dj_database_url.parse(config('DATABASE_URL'))
}


# AUTH BACKENDS
AUTHENTICATION_BACKENDS = [
   "django.contrib.auth.backends.AllowAllUsersModelBackend",
   "django.contrib.auth.backends.ModelBackend",
]


# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
   {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
   {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
   {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
   {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# LANGUAGE & TIMEZONE
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# STATIC FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Media files (Uploaded by users)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Cloudinary Storage
CLOUDINARY_STORAGE = {
   'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
   'API_KEY': config('CLOUDINARY_API_KEY'),
   'API_SECRET': config('CLOUDINARY_API_SECRET'),
}


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Optional: Use Cloudinary for static files too (if needed)
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
# Or keep WhiteNoise (default for most projects)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# LOGIN/LOGOUT
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/login/'


# SECURITY SETTINGS (Only enforced in production)
if not DEBUG:
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   SECURE_HSTS_SECONDS = 3600
   SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   SECURE_HSTS_PRELOAD = True


# MESSAGE TAGS (Bootstrap-compatible)
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
   messages.DEBUG: 'secondary',
   messages.INFO: 'info',
   messages.SUCCESS: 'success',
   messages.WARNING: 'warning',
   messages.ERROR: 'danger',
}


# REDIS CACHE (Optional)
CACHES = {
   "default": {
       "BACKEND": "django_redis.cache.RedisCache",
       "LOCATION": "redis://127.0.0.1:6379/1",
       "OPTIONS": {
           "CLIENT_CLASS": "django_redis.client.DefaultClient",
       }
   }
}


# DEFAULT AUTO FIELD
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'