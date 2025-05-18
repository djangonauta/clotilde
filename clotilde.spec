import os

block_cipher = None
base_dir = os.path.abspath(os.getcwd())

static_dir = os.path.join(base_dir, 'static')
templates_dir = os.path.join(base_dir, 'templates')

added_files = [
    ('_internal/static', 'static'),
    ('templates', 'templates'),
    ('db.sqlite3', '.'),
]

# Pacotes necessários que o PyInstaller pode não detectar automaticamente
hidden_imports = [
    'automacoes',
    'automacoes.views',
    'automacoes.urls',
    'automacoes.models',
    'automacoes.apps',
    'forms',
    'utils',
    'views',
    'django.template.defaulttags',
    'django.template.defaultfilters',
    'django.template.loader_tags',
    'django.templatetags',
    'django.templatetags.static',
    'django.templatetags.i18n',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.db.models.query',
    'django.db.models.expressions',
    'django.db.models.sql',
    'django.db.models.functions',
    'django.db.models.lookups',
    'django.db.models.aggregates',
    'webview',
    'webview.platforms.winforms',
    'webview.platforms.gtk',
    'widget_tweaks',
    'widget_tweaks.templatetags',
    'widget_tweaks.templatetags.widget_tweaks',
    'jinja2',
    'asgiref',
    'sqlparse',
]

a = Analysis(
    ['main.py'],
    pathex=[base_dir],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'notebook', 'scipy', 'pandas', 'PIL'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Criar o arquivo PYZ
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# Configuração do executável
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Clotilde',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon=os.path.join(base_dir, 'icon.ico'),
)

# Criação do pacote
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Clotilde',
)
