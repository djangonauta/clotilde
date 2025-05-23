import ctypes
import functools
import os
import os.path
import platform
import signal
import tkinter as tk
from tkinter import messagebox

from django import shortcuts


def sessao_possui_credenciais(view_func):
    @functools.wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'nome' in request.session and 'matricula' in request.session:
            return view_func(request, *args, **kwargs)

        return shortcuts.redirect('/login/')

    return _wrapped_view


def exibir_dialogo_esperar(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Informação", message)
    root.destroy()


def plataforma_windows():
    return platform.system().lower() == 'windows'


def caminho_driver_chrome():
    caminho = '~/chromedriver'
    if plataforma_windows():
        caminho += '.exe'

    return os.path.expanduser(caminho)


def pausar_processo(pid):
    try:
        if plataforma_windows():
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.OpenProcess(0x1F0FFF, False, pid)
            if handle:
                ntdll = ctypes.windll.ntdll
                ntdll.NtSuspendProcess(handle)
                kernel32.CloseHandle(handle)
                return True

        os.kill(pid, signal.SIGSTOP)
        return True

    except Exception as e:
        print('Erro ao pausar o processo', e)

    return False


def continuar_processo(pid):
    try:
        if plataforma_windows():
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.OpenProcess(0x1F0FFF, False, pid)
            if handle:
                ntdll = ctypes.windll.ntdll
                ntdll.NtResumeProcess(handle)
                kernel32.CloseHandle(handle)
                return True

        os.kill(pid, signal.SIGCONT)
        return True

    except Exception as e:
        print('Erro ao continuar o processo', e)

    return False


def cancelar_processo(processo):
    try:
        if plataforma_windows():
            os.kill(processo.pid, signal.SIGTERM)
            return True

        processo.terminate()
        return True

    except Exception as e:
        print('Erro ao cancelar o processo', e)

    return False
