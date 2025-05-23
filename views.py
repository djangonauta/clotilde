from django import shortcuts

import forms


# @utils.sessao_possui_credenciais
def index(request):
    return shortcuts.render(request, 'index.html', {
        'title': 'Bem vindo!!',
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
    })


def logout(request):
    request.session.flush()
    return shortcuts.redirect('/')
