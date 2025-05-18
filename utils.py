import functools
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
