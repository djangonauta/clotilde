"""
Arquivo de especificação PyInstaller para a aplicação Clotilde
Uma aplicação Django rodando dentro do PyWebview
"""
import os
import sys

from PyInstaller.utils.hooks import collect_all

block_cipher = None
base_dir = os.path.abspath(os.getcwd())

static_dir = os.path.join(base_dir, 'static')
templates_dir = os.path.join(base_dir, 'templates')

automacoes_imports, automacoes_datas, automacoes_binaries = collect_all('automacoes')

added_files = [
    ('static', 'static'),
    ('templates', 'templates'),
    ('db.sqlite3', '.'),
]

# Pacotes necessários que o PyInstaller pode não detectar automaticamente
hidden_imports = [
    'django',
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
    'webview.platforms.winforms',  # Para Windows
    'webview.platforms.cocoa',     # Para macOS
    'webview.platforms.gtk',       # Para Linux
    'jinja2',
    'asgiref',
    'sqlparse',
    'pytz',
] + automacoes_imports

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

# Para macOS, adicione esta configuração (opcional)
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='Clotilde.app',
        # icon=os.path.join(base_dir, 'icon.icns'),
        bundle_identifier='com.seudominio.clotilde',
        info_plist={
            'CFBundleShortVersionString': '1.0.0',
            'NSHighResolutionCapable': 'True',
        },
    )
