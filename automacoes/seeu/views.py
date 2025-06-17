import multiprocessing
import sys
import time
import traceback
import uuid

from django import http, shortcuts
from django.conf import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from automacoes import models, utils


def intimar_pessoalmente_a_partir_despacho(request):
    automacao = models.Automacao.objects.create(nome='Intimar pessoalmente a partir de despacho')
    id_processo = str(uuid.uuid4())

    processo = multiprocessing.Process(
        target=_intimar_pessoalmente_a_partir_despacho,
        args=(automacao.id, id_processo)
    )
    processo.start()

    settings.PROCESSOS[id_processo] = processo

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return http.JsonResponse({
            'status': 'success',
            'mensagem': 'Processamento iniciado',
            'id_automacao': automacao.id,
            'id_processo': id_processo,
        })

    return shortcuts.redirect('index')


def _intimar_pessoalmente_a_partir_despacho(id_automacao, id_processo):
    automacao = models.Automacao.objects.get(pk=id_automacao)
    try:
        driver = utils.obter_driver_chrome()
        driver.get(settings.SEEU_URL)
        janela_original = driver.current_window_handle

        wait = WebDriverWait(driver, 15)
        main_frame = wait.until(EC.visibility_of_element_located([By.ID, 'mainFrame']))

        driver.switch_to.frame(main_frame)
        botao = wait.until(EC.element_to_be_clickable([By.ID, 'btn-login-corporativo']))
        botao.click()

        janela_login_corporativo = WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        if janela_login_corporativo:
            # novas_abas = [janela for janela in driver.window_handles if janela != janela_original]
            # if novas_abas:
            janela_login = driver.window_handles[1]  # novas_abas[0]  # driver.window_handles[1] ?
            driver.switch_to.window(str(janela_login))

            campo_login = wait.until(EC.visibility_of_element_located([By.ID, 'username']))
            campo_login.send_keys('80644414200')

            campo_senha = wait.until(EC.visibility_of_element_located([By.ID, 'password']))
            campo_senha.send_keys('MiudoO5656@')

            botao_login = wait.until(EC.element_to_be_clickable([By.ID, 'kc-login']))
            botao_login.click()

        time.sleep(5)
        automacao.porcentagem = 10
        automacao.save()

        driver.switch_to.window(janela_original)
        driver.switch_to.frame(main_frame)

        xpath = ("//a[contains(text(), 'Execução') or contains(text(), 'Execuções') or contains(text(), "
                 "'Penal') or contains(text(), 'Penais')]")
        seletor_vara_criminal = (By.XPATH, xpath)
        primeira_vara_criminal = wait.until(EC.element_to_be_clickable(seletor_vara_criminal))
        primeira_vara_criminal.click()
        automacao.porcentagem = 20
        automacao.save()

        time.sleep(5)

        user_main_frame = wait.until(EC.visibility_of_element_located([By.ID, 'userMainFrame']))
        driver.switch_to.frame(user_main_frame)
        elemento = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[@name='tabOutrosCumprimentos']"))
        )
        elemento.click()

        xpath = "//tr[td[contains(text(), 'Mandado')]]/td[3]/a"
        elemento = wait.until(EC.element_to_be_clickable([By.XPATH, xpath]))
        elemento.click()

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'resultTable')))
        analisar_link = wait.until(
            EC.element_to_be_clickable([By.LINK_TEXT, "Analisar"])
        )
        analisar_link.click()

        time.sleep(10)
        automacao.porcentagem = 100
        automacao.status = models.Automacao.Status.FINALIZADA
        automacao.save()
        driver.quit()

    except Exception as e:
        automacao.status = models.Automacao.Status.ERRO
        automacao.stack_trace = ''.join(traceback.format_exception(*sys.exc_info()))
        automacao.save()

        driver.quit()
        utils.cancelar_processo(settings.PROCESSOS[id_processo])
        raise e
