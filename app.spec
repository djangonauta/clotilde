import os
import os.path

block_cipher = None
base_dir = os.path.abspath(os.getcwd())

added_files = [
    ('_internal/assets', 'assets'),
    ('templates', 'templates'),
    ('db.sqlite3', '.'),
]

excludes = [
    # Módulos de desenvolvimento e testes
    'unittest', 'doctest', 'pdb', 'pydoc',  # 'inspect',
    'debugpy', 'pytest', 'coverage',

    # Módulos científicos pesados (se não utilizados)
    'numpy', 'scipy', 'pandas', 'matplotlib', 'plotly',
    'seaborn', 'sklearn', 'tensorflow', 'torch',

    # Servidores web alternativos
    'gunicorn', 'uwsgi', 'waitress', 'cherrypy',
    'tornado', 'aiohttp', 'fastapi', 'flask',

    # Bancos de dados não utilizados
    'mysql', 'MySQLdb', 'pymysql', 'cx_Oracle',
    'pyodbc', 'redis', 'pymongo',
    'cassandra', 'elasticsearch',

    # Módulos do sistema operacional não necessários
    'curses', 'readline', 'rlcompleter',

    # Compiladores e ferramentas de build
    # 'distutils', 'setuptools', 'pip', 'wheel',
    # 'pkg_resources._vendor',

    # Ferramentas de documentação
    'sphinx', 'docutils', 'markdown',

    # Módulos de rede avançados
    'ftplib', 'imaplib', 'nntplib', 'poplib',
    'smtplib', 'telnetlib',

    # Módulos de compressão não essenciais
    # 'bz2', 'lzma', 'gzip',  'tarfile',

    # Processamento de imagem (se não utilizado)
    'PIL.ImageQt', 'PIL.ImageTk',

    # Módulos de criptografia avançada (manter apenas o necessário)
    'cryptography.hazmat.backends.openssl.x25519',
    'cryptography.hazmat.backends.openssl.x448',
    'cryptography.hazmat.backends.openssl.ed25519',
    'cryptography.hazmat.backends.openssl.ed448',
]

# Pacotes necessários que o PyInstaller pode não detectar automaticamente
hidden_imports = [
    'automacoes',
    'automacoes.views',
    'automacoes.urls',
    'automacoes.models',
    'automacoes.apps',
    'forms',
    'views',
    'django.template.defaulttags',
    'django.template.defaultfilters',
    'django.template.loader_tags',
    'django.templatetags',
    'django.templatetags.static',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.db.models.query',
    'webview',
    'webview.platforms.winforms',
    'widget_tweaks',
    'widget_tweaks.templatetags',
    'widget_tweaks.templatetags.widget_tweaks',
    'whitenoise',
    'whitenoise.middleware',
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
    excludes=excludes,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    exclude_binaries=True,
    name='Clotilde',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
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
