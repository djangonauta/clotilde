import os
import sys
import threading
import time
from wsgiref import simple_server

import webview

import dj

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def start_django_server():
    httpd = simple_server.make_server('0.0.0.0', 8000, dj.application)
    print('Servidor iniciado em http://0.0.0.0:8000')
    httpd.serve_forever()


class Api:
    def fullscreen(self):
        webview.windows[0].toggle_fullscreen()
        return True

    def minimize(self):
        webview.windows[0].minimize()
        return True

    def restore(self):
        webview.windows[0].restore()
        return True

    def get_version(self):
        return '1.0.0'


if __name__ == '__main__':
    t = threading.Thread(target=start_django_server)
    t.daemon = True
    t.start()

    time.sleep(1)

    window = webview.create_window(
        title='Clotilde',
        url='http://127.0.0.1:8000',
        js_api=Api(),
        width=1024,
        height=768,
        resizable=True,
        text_select=True,
        confirm_close=True,
        background_color='#FFFFFF'
    )
    webview.start(gui='qt')
