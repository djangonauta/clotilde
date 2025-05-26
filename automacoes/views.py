import multiprocessing
import sys
import time
import traceback
import uuid

from django import http, shortcuts
from django.conf import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from . import models, utils


def verificar_automacao(request, id_automacao):
    automacao = shortcuts.get_object_or_404(models.Automacao, pk=id_automacao)
    return http.JsonResponse({
        'status': automacao.status,
        'id_automacao': id_automacao,
        'porcentagem': automacao.porcentagem,
    })


def pausar_processo(request, id_processo):
    pid = settings.PROCESSOS[id_processo].pid
    utils.pausar_processo(pid)
    return http.JsonResponse({'mensagem': 'Processo pausado com sucesso'})


def continuar_processo(request, id_processo):
    pid = settings.PROCESSOS[id_processo].pid
    utils.continuar_processo(pid)
    return http.JsonResponse({'mensagem': 'Processo continuado com sucesso'})


def cancelar_processo(request, id_processo):
    processo = settings.PROCESSOS[id_processo]
    utils.cancelar_processo(processo)
    return http.JsonResponse({'mensagem': 'Processo sinalizado para finalização'})


def iniciar(request):
    automacao = models.Automacao.objects.create(nome='iniciar')
    id_processo = str(uuid.uuid4())
    processo = iniciar_processo(automacao.id)
    settings.PROCESSOS[id_processo] = processo
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return http.JsonResponse({
            'status': 'success',
            'mensagem': 'Processamento iniciado',
            'id_automacao': automacao.id,
            'id_processo': id_processo,
        })

    return shortcuts.redirect('index')


def iniciar_processo(id_automacao):
    p = multiprocessing.Process(target=tarefa, args=(id_automacao,))
    p.daemon = True
    p.start()
    return p


def tarefa(id_automacao):
    automacao = models.Automacao.objects.get(pk=id_automacao)
    try:
        driver = utils.obter_driver_chrome()
        driver.implicitly_wait(3)
        driver.get('https://demoqa.com/forms')
        driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div/ul/li/span'
        ).click()
        automacao.porcentagem = 10
        automacao.save()
        time.sleep(.5)

        driver.find_element(By.ID, 'firstName').send_keys('Igor')
        automacao.porcentagem = 20
        automacao.save()
        time.sleep(.5)

        driver.find_element(By.ID, 'lastName').send_keys('Carvalho')
        automacao.porcentagem = 30
        automacao.save()
        time.sleep(.5)
        driver.find_element(By.ID, 'userEmail').send_keys('igor.carvalho@tjpa.jus.br')
        automacao.porcentagem = 40
        automacao.save()
        time.sleep(.5)

        driver.find_element(By.CSS_SELECTOR, 'div.custom-radio:nth-child(3) > label:nth-child(2)').click()
        automacao.porcentagem = 50
        automacao.save()
        time.sleep(.5)

        data_nascimento = driver.find_element(By.ID, 'dateOfBirthInput')
        driver.execute_script("arguments[0].select();", data_nascimento)
        data_nascimento.send_keys('30 Sep 1983')
        data_nascimento.send_keys(Keys.ENTER)
        automacao.porcentagem = 60
        automacao.save()
        time.sleep(.5)

        driver.find_element(By.ID, 'userNumber').send_keys('91996418559')
        subjects = driver.find_element(By.ID, 'subjectsInput')
        subjects.send_keys('computer')
        subjects.send_keys(Keys.ENTER)
        automacao.porcentagem = 70
        automacao.save()
        time.sleep(.5)

        driver.find_element(By.CSS_SELECTOR, 'div.custom-checkbox:nth-child(1) > label:nth-child(2)').click()
        driver.execute_script("document.getElementById('submit').click()")
        automacao.porcentagem = 100
        automacao.save()
        time.sleep(.5)

        # utils.exibir_dialogo_esperar('Automação finalizada')

        driver.find_element(By.ID, 'closeLargeModal').click()
        driver.quit()

        automacao.status = models.Automacao.Status.FINALIZADA
        automacao.save()
        time.sleep(.5)

    except Exception as e:
        automacao.status = models.Automacao.Status.ERRO
        automacao.stack_trace = ''.join(traceback.format_exception(*sys.exc_info()))
        automacao.save()
        raise e
