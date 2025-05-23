from django import shortcuts
from django.conf import settings

import forms
import utils


# @utils.sessao_possui_credenciais
def index(request):
    return shortcuts.render(request, 'index.html', {
        'title': 'Bem vindo!!',
        'base_dir': settings.BASE_DIR,
    })


def login(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            form.salvar_dados_sessao(request)
            return shortcuts.redirect('/')

    return shortcuts.render(request, 'login.html', {
        'form': form,
        'base_dir': settings.BASE_DIR,
        'static_root': settings.STATIC_ROOT,
    })


def logout(request):
    request.session.flush()
    return shortcuts.redirect('/')
