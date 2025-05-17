import sys
from pathlib import Path

import django
from django.conf import settings
from django.conf.urls import static
from django.core.wsgi import get_wsgi_application
from django.urls import path

import views

BASE_DIR = Path(__file__).resolve().parent
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent

TEMPLATE_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
DB_PATH = BASE_DIR / 'db.sqlite3'

settings.configure(
    DEBUG=True,
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
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
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
    ALLOWED_HOSTS=['*'],
)

django.setup()

urlpatterns = [
    path('', views.index, name='index'),
    path('tarefa/', views.selenium, name='selenium'),
]
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
