import multiprocessing
import time
import uuid

from django import http
from django.conf import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

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
    return http.JsonResponse({
        'status': 'success',
        'mensagem': 'Processamento iniciado',
        'id_automacao': automacao.id,
        'id_processo': id_processo,
    })


def _intimar_pessoalmente_a_partir_despacho(id_automacao, id_processo):
    automacao = models.Automacao.objects.get(pk=id_automacao)
    try:
        driver = utils.obter_driver_chrome()
        driver.get(settings.SEEU_URL)
        janela_original = driver.current_window_handle

        wait = WebDriverWait(driver, 15)
        main_frame = mudar_para_main_frame(driver, wait)

        clicar_botao_login_corporativo(wait)

        janela_login_corporativo = WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        if janela_login_corporativo:
            mudar_para_janela_login(driver)
            efetuar_login(wait)

        atualizar_porcentagem(automacao, 5)

        mudar_para_janela_original(driver, janela_original, main_frame)
        atualizar_porcentagem(automacao, 10)

        selecionar_vara(wait)
        atualizar_porcentagem(automacao, 15)

        mudar_para_user_main_frame(driver, wait)

        clicar_tab_outros_cumprimentos(wait)
        atualizar_porcentagem(automacao, 20)

        clicar_link_mandados(wait)
        atualizar_porcentagem(automacao, 25)

        clicar_link_analisar(wait)
        atualizar_porcentagem(automacao, 30)

        selecionar_tipo_arquivo_mandado(wait)
        atualizar_porcentagem(automacao, 35)

        selecionar_modelo_mandado(wait)
        atualizar_porcentagem(automacao, 40)

        clicar_botao_digitar_texto(wait)
        atualizar_porcentagem(automacao, 45)

        clicar_botao_continuar(wait)
        atualizar_porcentagem(automacao, 50)

        clicar_botao_salvar(wait)
        atualizar_porcentagem(automacao, 55)

        clicar_botao_concluir(wait)
        atualizar_porcentagem(automacao, 60)

        clicar_botao_alterar(wait)
        atualizar_porcentagem(automacao, 65)

        preencher_form_cumprimento(wait)
        atualizar_porcentagem(automacao, 70)

        clicar_botao_salvar_form_cumprimento(wait)
        atualizar_porcentagem(automacao, 75)

        clicar_botao_adicionar(wait)
        atualizar_porcentagem(automacao, 80)

        mudar_para_modal_frame(driver, wait)

        selecionar_arquivo_decisao(wait)
        atualizar_porcentagem(automacao, 85)

        clicar_botao_selecionar(wait)
        atualizar_porcentagem(automacao, 90)

        mudar_para_user_main_frame(driver, wait)

        clicar_botao_postergar_assinatura(wait)
        atualizar_porcentagem(automacao, 5)

        atualizar_porcentagem(automacao, 100, sleep=15, status=models.Automacao.Status.FINALIZADA)
        driver.quit()

    except Exception as e:
        utils.tratar_erro_automacao(automacao, id_processo)
        driver.quit()
        raise e


def mudar_para_main_frame(driver, wait):
    main_frame = wait.until(EC.visibility_of_element_located([By.ID, 'mainFrame']))
    driver.switch_to.frame(main_frame)
    return main_frame


def clicar_botao_login_corporativo(wait):
    botao = wait.until(EC.element_to_be_clickable([By.ID, 'btn-login-corporativo']))
    botao.click()


def atualizar_porcentagem(automacao, porcentagem, status=None, sleep=3):
    automacao.porcentagem = porcentagem
    if status:
        automacao.status = status

    automacao.save()
    if sleep:
        time.sleep(sleep)


def mudar_para_janela_login(driver):
    janela_login = driver.window_handles[1]
    driver.switch_to.window(str(janela_login))


def efetuar_login(wait):
    campo_login = wait.until(EC.visibility_of_element_located([By.ID, 'username']))
    campo_login.send_keys(settings.USUARIO_SEEU)

    campo_senha = wait.until(EC.visibility_of_element_located([By.ID, 'password']))
    campo_senha.send_keys(settings.SENHA_SEEU)

    botao_login = wait.until(EC.element_to_be_clickable([By.ID, 'kc-login']))
    botao_login.click()


def mudar_para_janela_original(driver, janela_original, main_frame):
    driver.switch_to.window(janela_original)
    driver.switch_to.frame(main_frame)


def selecionar_vara(wait):
    xpath = ("//a[contains(text(), 'Execução') or contains(text(), 'Execuções') or contains(text(), "
             "'Penal') or contains(text(), 'Penais')]")
    seletor_vara_criminal = (By.XPATH, xpath)
    primeira_vara_criminal = wait.until(EC.element_to_be_clickable(seletor_vara_criminal))
    primeira_vara_criminal.click()


def mudar_para_user_main_frame(driver, wait):
    user_main_frame = wait.until(EC.visibility_of_element_located([By.ID, 'userMainFrame']))
    driver.switch_to.frame(user_main_frame)
    return user_main_frame


def clicar_tab_outros_cumprimentos(wait):
    elemento = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@name='tabOutrosCumprimentos']")))
    elemento.click()


def clicar_link_mandados(wait):
    xpath = "//tr[td[contains(text(), 'Mandado')]]/td[3]/a"
    wait.until(EC.element_to_be_clickable([By.XPATH, xpath])).click()


def clicar_link_analisar(wait):
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'resultTable')))
    wait.until(EC.element_to_be_clickable([By.LINK_TEXT, "Analisar"])).click()


def selecionar_tipo_arquivo_mandado(wait):
    wait.until(EC.visibility_of_element_located([By.ID, 'descricaoTipoArquivo'])).send_keys('Mandado')
    wait.until(EC.visibility_of_element_located((By.ID, 'ajaxAuto_descricaoTipoArquivo')))
    wait.until(EC.element_to_be_clickable((By.ID, '101'))).click()


def selecionar_modelo_mandado(wait):
    (wait.until(EC.visibility_of_element_located([By.ID, 'descricaoModelo']))
         .send_keys('MANDADO - LIVRAMENTO CONDICIO'))
    wait.until(EC.visibility_of_element_located((By.ID, 'ajaxAuto_descricaoModelo')))
    wait.until(EC.element_to_be_clickable((By.ID, '609404'))).click()


def clicar_botao_digitar_texto(wait):
    wait.until(EC.element_to_be_clickable([By.ID, 'digitarButton'])).click()


def clicar_botao_continuar(wait):
    wait.until(EC.element_to_be_clickable([By.ID, 'submitButton'])).click()


def clicar_botao_salvar(wait):
    wait.until(EC.element_to_be_clickable([By.CSS_SELECTOR, 'input[value="Salvar"]'])).click()


def clicar_botao_concluir(wait):
    wait.until(EC.element_to_be_clickable([By.ID, 'finishButton'])).click()


def clicar_botao_alterar(wait):
    wait.until(EC.element_to_be_clickable(
        [By.XPATH, '//input[@id="editButton" and @value="Alterar"]'])).click()


def preencher_form_cumprimento(wait):
    xpath = '/html/body/div[1]/div[3]/form/fieldset/table[1]/tbody/tr[6]/td[2]/label[1]/input'
    wait.until(EC.element_to_be_clickable([By.XPATH, xpath])).click()

    prazo = wait.until(EC.element_to_be_clickable([By.ID, 'prazoOficialJustica']))
    prazo.clear()
    prazo.send_keys('15')

    css_selector = 'input[type="radio"][name="codTipoClassificacaoMandado"][value="1"]'
    wait.until(EC.element_to_be_clickable([By.CSS_SELECTOR, css_selector])).click()

    select_element = wait.until(EC.presence_of_element_located((By.ID, "codCustasMandado")))
    select = Select(select_element)
    select.select_by_value("1")


def clicar_botao_salvar_form_cumprimento(wait):
    wait.until(EC.element_to_be_clickable([By.ID, 'saveButton'])).click()


def clicar_botao_adicionar(wait):
    wait.until(EC.element_to_be_clickable([By.ID, 'editButton'])).click()


def mudar_para_modal_frame(driver, wait):
    css_selector = "[name^='window_'][name$='_content']"
    modal_frame = wait.until(EC.presence_of_element_located([By.CSS_SELECTOR, css_selector]))
    driver.switch_to.frame(modal_frame)
    return modal_frame


def selecionar_arquivo_decisao(wait):
    wait.until(EC.element_to_be_clickable([By.NAME, 'movimentacoesArquivos'])).click()


def clicar_botao_selecionar(wait):
    wait.until(EC.element_to_be_clickable([By.ID, 'selectButton'])).click()


def clicar_botao_postergar_assinatura(wait):
    wait.until(EC.element_to_be_clickable([By.ID, 'postergarButton'])).click()
