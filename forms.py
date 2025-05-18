from django import forms
from django.core import exceptions


class LoginForm(forms.Form):
    nome = forms.CharField(max_length=100)
    matricula = forms.CharField(max_length=20)

    def clean_nome(self):
        nome = self.cleaned_data['nome']
        if len(nome) <= 3:
            raise exceptions.ValidationError('Nome deve possuir mais que 3 caracteres')

        return nome

    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        try:
            int(matricula)
            return matricula

        except ValueError:
            raise exceptions.ValidationError('Matrícula deve possuir apenas números')

    def salvar_dados_sessao(self, request):
        request.session['nome'] = self.cleaned_data['nome']
        request.session['matricula'] = self.cleaned_data['matricula']
