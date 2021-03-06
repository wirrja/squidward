"""
Django settings for pytopo project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7kpop@3fy&m68rrhwnwdi6w^n&+*nr&ywe=qsst1x%gze4cpr@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django_celery_beat',
    'django_celery_results',
    'bootstrap3',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # pytopo`s apps
    'squidward.apps.SquidwardConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pytopo.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'pytopo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'squidward',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USER': 'squidward',
        'PASSWORD': 'Parolsquidward#',
        'CONN_MAX_AGE': 600,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 86400,
    }
 }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

LOGIN_URL = '/admin/login/'
# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


# Celery config
CELERY_BROKER_URL = 'amqp://celery:celerypassword@localhost:5672/squidward'
CELERY_RESULT_BACKEND = 'amqp://celery:celerypassword@localhost:5672/squidward'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'

from celery.schedules import crontab, schedule
# crontab tasks
CELERY_BEAT_SCHEDULE = {
    'write-csv-for-postgres': {
        'task': 'squidward.tasks.task_write_csv_postgresql',
        'schedule': crontab(minute=20, hour=2),
    },
    'copy-csv-to-postgres': {
        'task': 'squidward.tasks.task_copy_csv_postgresql',
        'schedule': crontab(minute=1, hour=3),
    },
    'delete-old-data-postgres': {
        'task': 'squidward.tasks.task_delete_old_data',
        'schedule': crontab(minute=1, hour=5)
    },
    'download-logs-sftp' :{
        'task': 'squidward.tasks.task_download_logs_sftp',
        'schedule': crontab(minute=1, hour=2)
    }
}

# for celery`s nightly COPY to PostgreSQL
#SQUID_LOGDIR = '/home/pi/code/logs/'
SQUID_LOGDIR = '/home/dds/squidward/squidlogs/'
CSV_FILE = SQUID_LOGDIR + 'copy_psql.csv'
CSV_FILE_MESSAGES_WHITE = SQUID_LOGDIR + 'copy_psql_white.csv'
CSV_FILE_MESSAGES_GRAY = SQUID_LOGDIR + 'copy_psql_gray.csv'

# data lifetime in database (seconds) default - 32 days
DB_STORE_TIME = 2764800
PPTP_LOGDIR_REMOTE = '/var/log/'
SQUID_LOGDIR_REMOTE = '/var/log/squid/'
SQUID_USERNAME = ''
SQUID_PASSWORD = ''
LOG_FILENAME = [
    'access', 'message'
]
