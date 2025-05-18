import os
import sys

import django
from django import urls
from django.conf import settings
from django.conf.urls import static
from django.core.wsgi import get_wsgi_application

import views

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')

settings.configure(
    DEBUG=DEBUG,
    BASE_DIR=BASE_DIR,
    SECRET_KEY='your-secret-key-here',
    ROOT_URLCONF=__name__,
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
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
    STATIC_URL='_internal/static/',
    STATICFILES_DIRS=[STATIC_DIR],
    ALLOWED_HOSTS=['*'],
)

django.setup()

urlpatterns = [
    urls.path('', views.index, name='index'),
    urls.path('login/', views.login, name='login'),
    urls.path('logout/', views.logout, name='logout'),
    urls.path('automacoes/', urls.include('automacoes.urls')),
]
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
