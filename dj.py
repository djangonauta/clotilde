import os
import sys

import django
from django import urls
from django.conf import settings
from django.conf.urls import static
from django.core.management.utils import get_random_secret_key
from django.core.wsgi import get_wsgi_application

import views

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    DEBUG = False

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '_internal/static')
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')

settings.configure(
    DEBUG=DEBUG,
    BASE_DIR=BASE_DIR,
    SECRET_KEY=get_random_secret_key(),
    ROOT_URLCONF=__name__,
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        "whitenoise.middleware.WhiteNoiseMiddleware",
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    INSTALLED_APPS=[
        'automacoes',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'widget_tweaks',
    ],
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    }],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DB_PATH,
        }
    },
    STATIC_URL='/static/',
    STATICFILES_DIRS=[STATIC_DIR],
    STATIC_ROOT='_internal/assets/',
    ALLOWED_HOSTS=['localhost', '127.0.0.1'],
    PROCESSOS={},
)

django.setup()

urlpatterns = [
    urls.path('', views.index, name='index'),
    urls.path('login/', views.login, name='login'),
    urls.path('logout/', views.logout, name='logout'),
    urls.path('automacoes/', urls.include('automacoes.urls')),
]
if DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
