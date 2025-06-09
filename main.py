import multiprocessing
import os
import sys
import time

import waitress

import dj

LOGO = """

  ██████╗██╗      ██████╗ ████████╗██╗██╗     ██████╗ ███████╗
 ██╔════╝██║     ██╔═══██╗╚══██╔══╝██║██║     ██╔══██╗██╔════╝
 ██║     ██║     ██║   ██║   ██║   ██║██║     ██║  ██║█████╗
 ██║     ██║     ██║   ██║   ██║   ██║██║     ██║  ██║██╔══╝
 ╚██████╗███████╗╚██████╔╝   ██║   ██║███████╗██████╔╝███████╗
  ╚═════╝╚══════╝ ╚═════╝    ╚═╝   ╚═╝╚══════╝╚═════╝ ╚══════╝

              Automação Desktop :: TJPA
"""

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def abrir_navegador(host='127.0.0.1', porta=8000, atraso=2):
    time.sleep(atraso)
    url = f'http://{host}:{porta}'
    try:
        chrome_path = None
        chrome_locations = [
            # Caminhos em inglês
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',

            # Caminhos em português do Brasil
            r'C:\Arquivos de Programas\Google\Chrome\Application\chrome.exe',
            r'C:\Arquivos de Programas (x86)\Google\Chrome\Application\chrome.exe',

            # Caminhos do usuário (funciona em qualquer idioma)
            r'C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe'.format(
                os.environ.get('USERNAME', '')),

            # Variações de variáveis de ambiente
            r'C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe'.format(
                os.environ.get('USUARIO', os.environ.get('USERNAME', ''))),

            # Caminho alternativo do usuário
            r'{}\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'.format(
                os.environ.get('USERPROFILE', '')),
        ]

        for location in chrome_locations:
            if os.path.exists(location):
                chrome_path = location
                break

        if chrome_path:
            import subprocess
            chrome_args = [
                chrome_path,
                '--new-window',
                '--window-size=1024,768',
                '--window-position=100,100',
                # '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                url
            ]
            subprocess.Popen(chrome_args)

    except Exception as e:
        print(f'⚠️ Erro ao abrir navegador: {e}')


def start_django_server():
    print(LOGO)
    waitress.serve(dj.application, host='127.0.0.1', port=8000, threads=6)


def main():
    multiprocessing.freeze_support()
    t = multiprocessing.Process(target=abrir_navegador)
    t.daemon = True
    t.start()

    start_django_server()


if __name__ == '__main__':
    main()
