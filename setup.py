import sys
from pathlib import Path

from cx_Freeze import Executable, setup

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
DB_PATH = BASE_DIR / 'db.sqlite3'


build_exe_options = {
    'packages': ['os', 'sys', 'django', 'threading', 'time', 'wsgiref', 'pathlib'],
    'includes': [
        'django.template.defaulttags',
        'django.template.defaultfilters',
        'django.template.loader_tags',
    ],
    'include_files': [TEMPLATES_DIR, STATIC_DIR, DB_PATH],
}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(
    name='MeuAppDjango',
    version='0.1',
    description='Aplicação Django em arquivo único',
    options={'build_exe': build_exe_options},
    executables=[Executable('main.py', base=base)]
)
