from django import http, shortcuts
from django.conf import settings

from . import models, utils

SUCESSO = 2
ERRO = 3


def verificar_automacao(request, id_automacao):
    automacao = shortcuts.get_object_or_404(models.Automacao, pk=id_automacao)
    return http.JsonResponse({
        'status': automacao.status,
        'id_automacao': id_automacao,
        'porcentagem': automacao.porcentagem,
        'stack_trace': automacao.stack_trace[-200:],
    })


def pausar_processo(request, id_processo):
    processo = settings.PROCESSOS.get(id_processo, None)
    data = {'mensagem': 'Processo não encontrado', 'status': ERRO}
    if processo:
        utils.pausar_processo(processo.pid)
        data = {'mensagem': 'Processo pausado com sucesso', 'status': SUCESSO}

    return http.JsonResponse(data)


def continuar_processo(request, id_processo):
    processo = settings.PROCESSOS.get(id_processo, None)
    data = {'mensagem': 'Processo não encontrado', 'status': ERRO}
    if processo:
        utils.continuar_processo(processo.pid)
        data = {'mensagem': 'Processo continuado com sucesso', 'status': SUCESSO}

    return http.JsonResponse(data)


def cancelar_processo(request, id_processo):
    processo = settings.PROCESSOS.get(id_processo, None)
    data = {'mensagem': 'Processo não encontrado', 'status': ERRO}
    if processo:
        utils.cancelar_processo(processo)
        data = {'mensagem': 'Processo sinalizado para finalização', 'status': SUCESSO}

    return http.JsonResponse(data)
