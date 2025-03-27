"""
Configurações principais do projeto Django
--------------------------------------------
Este arquivo define as configurações do projeto, incluindo caminhos, segurança,
aplicativos instalados, banco de dados, internacionalização, arquivos estáticos,
e configurações de logging. Consulte a documentação oficial do Django para
mais detalhes: https://docs.djangoproject.com/en/5.1/
"""

import os
from decouple import config
from pathlib import Path
import logging  # noqa: F401
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from django import apps  # noqa: F401

# =============================================================================
# Caminhos do Projeto
# =============================================================================
# Define o diretório base do projeto para facilitar a construção de caminhos relativos.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# Configurações de Segurança e Ambiente
# =============================================================================
# Chave secreta usada em produção. Mantenha-a oculta!
SECRET_KEY = config('SECRET_KEY')

# Modo de depuração. Nunca habilite DEBUG em produção.
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos (lista de domínios ou endereços IP autorizados a acessar o site)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
LOGIN_URL = '/login/'
# =============================================================================
# Backends de Autenticação
# =============================================================================
# Permite a utilização de autenticação personalizada via e-mail além do backend padrão.
AUTHENTICATION_BACKENDS = [
    "apps.accounts.backends.EmailBackend",  # Autenticação via e-mail
    "django.contrib.auth.backends.ModelBackend",  # Backend padrão do Django
]

# =============================================================================
# Aplicativos Instalados
# =============================================================================
INSTALLED_APPS = [
    # Apps padrão do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps personalizados
    'apps.accounts',
    'apps.lojas',
   
    # Apps de terceiros (adicione conforme necessário)
]

# =============================================================================
# Middleware
# =============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =============================================================================
# URLs, Templates e WSGI
# =============================================================================
ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Diretório para templates personalizados
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'core.wsgi.application'

# =============================================================================
# Banco de Dados
# =============================================================================
# Em ambiente de desenvolvimento utiliza SQLite; em produção utiliza PostgreSQL.
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='mydatabase'),
            'USER': config('DB_USER', default='myuser'),
            'PASSWORD': config('DB_PASSWORD', default='mypassword'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# =============================================================================
# Validação de Senhas
# =============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =============================================================================
# Internacionalização e Fuso Horário
# =============================================================================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# =============================================================================
# Arquivos Estáticos e Mídia
# =============================================================================
# Configurações de arquivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Configurações de arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Utiliza Whitenoise para compressão e cache busting dos arquivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Localizadores de arquivos estáticos (encontra arquivos em diretórios especificados)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# =============================================================================
# Campo Primário Padrão
# =============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# Configuração de Autenticação Personalizada
# =============================================================================
AUTH_USER_MODEL = 'accounts.Usuario'

# =============================================================================
# Configurações de E-mail
# =============================================================================
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# =============================================================================
# Configurações do Celery (Tarefas Assíncronas)
# =============================================================================
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')

# =============================================================================
# Configurações do Redis
# =============================================================================
REDIS_HOST = config('REDIS_HOST', default='localhost')
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
REDIS_DB = config('REDIS_DB', default=0, cast=int)

# =============================================================================
# Configurações de Logging
# =============================================================================
# Diretório onde os arquivos de log serão armazenados
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)  # Garante que o diretório exista

# Configuração básica de logging com rotação de arquivos
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # Roda logs com base no tamanho do arquivo
            'filename': os.path.join(LOG_DIR, 'debug.log'),
            'maxBytes': 10 * 1024 * 1024,  # Limite de 10 MB por arquivo
            'backupCount': 5,  # Mantém 5 backups dos arquivos de log
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'loggers': {
        # Logger para o Django
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        # Logger para o backend do banco de dados do Django
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
        # Logger específico para o app 'usuarios'
        'usuarios': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# =============================================================================
# Configurações Alternativas de Logging (comentadas)
# =============================================================================
"""
Exemplo de configuração de logging mais avançada que inclui logs para o console
e arquivos separados para debug e erros. Pode ser habilitado se necessário.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] [{levelname}] [{name}] {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
            'maxBytes': 5 * 1024 * 1024,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'when': 'midnight',
            'backupCount': 30,  # Mantém os logs de erro por 30 dias
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_debug', 'file_error', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
"""
