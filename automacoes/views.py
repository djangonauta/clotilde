import multiprocessing
import os.path
import sys
import time
import traceback
import uuid
import logging

from django import http, shortcuts
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

import utils
import time
import re
import copy

from . import models

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


# def verificar(request, id_automacao):
#     automacao = shortcuts.get_object_or_404(models.Automacao, pk=id_automacao)
#     return http.JsonResponse({
#         'status': automacao.status,
#         'id_automacao': id_automacao,
#         'porcentagem': automacao.porcentagem,
#     })


def cancelar(request, id_processo):
    settings.PROCESSOS[id_processo].terminate()
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
    p = multiprocessing.Process(target=loginSeeu, args=(id_automacao,))
    p.daemon = True
    p.start()
    return p


def tarefa(id_automacao):
    automacao = models.Automacao.objects.get(pk=id_automacao)
    try:
        options = Options()
        driver = webdriver.Chrome(
            service=Service(os.path.expanduser('~/chromedriver')),
            options=options,
        )
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

        utils.exibir_dialogo_esperar('Automação finalizada')

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
    
def configurar_driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins-discovery")
    
    return webdriver.Chrome(
            service=Service(os.path.expanduser('~/chromedriver')),
            options=options,
        )
    
    
def loginSeeu(id_automacao):
    driver = configurar_driver()
    driver.get('https://seeuintegra.pje.jus.br/seeu/')
    
    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mainFrame'))
        )
        
        driver.switch_to.frame(iframe)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a#btn-login-corporativo')))
        # driver.find_element(By.ID, "btn-login-senha-toogle").click()
        # driver.find_element(By.ID, "login").send_keys('rodrigo.resque')
        # driver.find_element(By.ID, "senha").send_keys('123456')
        # driver.find_element(By.ID, 'login-form').find_element(By.ID, 'btEntrar').click()

        janela_original = driver.current_window_handle
        driver.find_element(By.ID, "btn-login-corporativo").click()
        
        corporaivo = WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        if corporaivo:
            todas_janelas = driver.window_handles
            novas_abas = [ janela for janela in todas_janelas if janela != janela_original]
            
            if novas_abas:
                nova_aba = novas_abas[0]
                
                if not isinstance(nova_aba, str):
                    nova_aba = str(nova_aba)
                
                time.sleep(1.0)
                
                driver.switch_to.window(str(nova_aba))
                
                driver.find_element(By.ID, "username").send_keys('89858948204')
                driver.find_element(By.ID, "password").send_keys('Ro5291204.,')
                driver.find_element(By.ID, "kc-login").click()
                
                time.sleep(0.5)
                
                janela_atual_seeu = driver.current_window_handle
                todas_janelas_atualis = driver.window_handles
                novas_abas_atuais = [ janela_atual for janela_atual in todas_janelas_atualis if janela_atual != janela_atual_seeu]
                
                if novas_abas_atuais:
                    nova_aba_atual = novas_abas_atuais[0]
                    
                    if not isinstance(nova_aba_atual, str):
                        nova_aba_atual = str(nova_aba_atual)
                        
                    driver.switch_to.window(nova_aba_atual)
                
                    logging.info(f'Url atual: {driver.current_url}')
                    logging.info('Etapa de autenticacao finalizada')
                    
                    continua_seeu_apos_login(driver)
    except Exception as e:
        print(f"Erro ao acessar elementos na nova aba: {e}")
        driver.close()
    
    
def debug_elemento(elemento, prefixo=""):
    """Debug rápido de elemento"""
    
    attrs = []
    for attr in ['id', 'class', 'tag', 'type']:
        val = elemento.get_attribute(attr)
        if val:
            attrs.append(f"{attr}={val}")
    
    texto = elemento.text.strip()[:30]
    status = "✅" if elemento.is_displayed() else "❌"
    
    linha = f"{prefixo}{status} {elemento.tag_name}({', '.join(attrs)})"
    if texto:
        linha += f" → '{texto}'"
    
    print(linha)


def existe_id(driver, id_element, timout=10):
    try:
        elemento = WebDriverWait(driver, timout).until(
                EC.presence_of_element_located((By.ID, id_element)))
        debug_elemento(elemento, id_element)
        return True
    except:
        return False
    

def existe_elemento(driver, locator_value, locator_type="id", timeout=10):
    locator_map = {
        'id': By.ID,
        'class': By.CLASS_NAME,
        'xpath': By.XPATH,
        'css': By.CSS_SELECTOR,
        'name': By.NAME,
        'tag': By.TAG_NAME,
        'link_text': By.LINK_TEXT,
        'partial_link_text': By.PARTIAL_LINK_TEXT
    }
    
    try:
        locator_type_lower = locator_type.lower()
        if locator_type_lower not in locator_map:
            raise ValueError(f"O Tipo de localizador '{locator_type}' não é válido.")
        
        by_locator = locator_map[locator_type_lower]
        
        WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by_locator, locator_value)))
      
        return True
    except Exception as e:
        logger.error(f"Elemento não encontrado: {locator_type}='{locator_value}' - {str(e)}")
        return False
    
    
def acessar_elemento(driver, locator_value, locator_type="id", timout=10):
    locator_map = {
        'id': By.ID,
        'class': By.CLASS_NAME,
        'xpath': By.XPATH,
        'css': By.CSS_SELECTOR,
        'tag': By.TAG_NAME
    }
    
    by_locator = locator_map[locator_type.lower()]
    elemento = WebDriverWait(driver, timout).until(
        EC.presence_of_element_located((by_locator, locator_value))
    )
    debug_elemento(elemento)
    
    return elemento
    
    
def acessar_elementos(driver, locator_value, locator_type="id", timout=10) -> list:
    locator_map = {
        'id': By.ID,
        'class': By.CLASS_NAME,
        'xpath': By.XPATH,
        'css': By.CSS_SELECTOR,
        'tag': By.TAG_NAME
    }
    
    by_locator = locator_map[locator_type.lower()]
    
    try: 
        WebDriverWait(driver, timout).until(
            EC.presence_of_element_located((by_locator, locator_value))
        )
        elementos = driver.find_elements(by_locator, locator_value)
        
        for elemento in elementos:
            debug_elemento(elemento)
        
        return elementos
    except Exception as e:
        logger.error(f'Nenhum elemento encontrado: {e}')
        return []
    


  
def continua_seeu_apos_login(driver):
    try:
        logging.info(driver)
        if existe_elemento(driver, 'mainFrame'):
            iframe = acessar_elemento(driver, 'mainFrame')        
            driver.switch_to.frame(iframe)
            
            driver = acessar_lista_atuacao(driver) #l:619 (method: automacao) (TaskIntimarPessoalmente_SEEU_11)
            
            if not driver:
                raise Exception('Falha ao mudar de vara')
            
            logger.info('Acessou a mesa do analista') #l:628
            
            continuacao = True
            while continuacao:
                continuacao = False
                # PÁGINA 1
                quantidade = pagina_1(driver)
                if quantidade > 0:
                    quantidade = True
                    logger.info(f'Finalizou Página 1 com quantidade {quantidade}')
                    processo = pagina_2(driver)
                    logger.info(f'Finalizou pagina_2, processo: {processo}')
                    # TODO Aqui entraria a parte do log e geração de arquivo em excell
                    try:
                        pagina_3(driver) #l:649 (TaskIntimarPessoalmente_SEEU_11)
                    except Exception as e:
                        # TODO Caso ocorra excessão enviar error para o log.
                        pass
                        
                    try:
                        pagina_4(driver)
                        logger.info(f'Finalizou pagina_4, processo: {processo}')
                    except Exception as e:
                        # TODO Caso ocorra excessão enviar error para o log.
                        pass
            
            
    except Exception as e:
        logger.error(e)
        logger.info('Ocorreu uma falha ao autenticar')
    
    logger.info('Acessou SEEU')
    
    time.sleep(2)
    
    
def selecionar_perfil_seeu(driver):
    """
        Seleção de Perfil no SEEU
    """
    try:
        if existe_elemento(driver, '//a[contains(text(), "Analista Judiciário")]', 'xpath'):
            WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '//a[contains(text(), "Analista Judiciário")]'))).click()

            logging.info('Clicando no perfil Analista Judiciário')
    except Exception as e:
        logging.info('Nao foi possivel selecionar o perfil')
        logging.info('Continuando . . .')
        
        
def acessar_lista_atuacao(driver): #l:526 (ExecuteAlteraVara - TaskIntimarPessoalmente_SEEU_011)
    locator_value = 'listaAreavara'
    if existe_elemento(driver, locator_value):
        locator_value = f"#{locator_value} li"
        locator_type = 'css'
        elementos = acessar_elementos(driver, locator_value, locator_type)
        result = acessar_vara(driver, elementos) # l:528 (TaskIntimarPessoalmente_SEEU_011.PY)
        
        if not result:
            logger.info('Nao foi possivel alterar a vara')
            logger.info('Finalizando robo')
            
            return result
        
        return driver
 
def filtrar_por_varas_excecucoes_penais(nome_vara):
    paradrao_explicito =  r'\b(Execução|Execuções|Penal|Penais)\b'
    
    return re.findall(paradrao_explicito, nome_vara, re.IGNORECASE)       

def acessar_vara(driver, elementos):
    locator_value = 'a'
    locator_type = 'tag'
    for elemento in elementos:
        if existe_elemento(elemento, locator_value, locator_type):
            logger.info(f'Acessando a vara: {debug_elemento(elemento)}')
            acessar_elemento(elemento, locator_value, locator_type).click()
            driver.switch_to.default_content()
            locator_value = 'mainFrame'
            if existe_elemento(driver, locator_value):
                main_frame = acessar_elemento(driver, locator_value)
                driver.switch_to.frame(main_frame)
                
                logger.info('Recarregar os elementos na tela de varas')
                
                time.sleep(0.5)
                
                # Abre o primeiro shadowroot
                shadow_host_01 = driver.find_element(By.CSS_SELECTOR, '#header')
                shadow_root_01 = shadow_host_01.shadow_root
                
                logger.info('Abre novamente o shadow root')
                
                # Elemento de texto começa a partir do terceiro filho
                count = 3
                
                try:
                    while True:
                        # Localiza a vara a ser trocada
                        select_result = shadow_root_01.find_element(By.CSS_SELECTOR,
                            'div.flex-grow seeu-dropdown seeu-menu-item:nth-child(' + str(count) + ')').text
                        
                        nome_vara = str(select_result).strip()
                        if nome_vara:
                            filtro_vara = filtrar_por_varas_excecucoes_penais(nome_vara)
                            if len(filtro_vara) > 0:
                                element_in_shadow = shadow_root_01.find_element(By.CSS_SELECTOR,
                                                        'div.flex-grow seeu-dropdown seeu-menu-item:nth-child(' + str(count) + ')')
                                
                                driver.execute_script("arguments[0].click();", element_in_shadow)
                                logger.info(f'Nome da Vara: {nome_vara}')
                                
                                break
                            else:
                                count += 1
                            
                except Exception as e:
                    logger.info(repr(e))
                    logger.info(f'Não foi possivel localizar a vara informada: {nome_vara}')
                    
                    return False
                
                return True
                    
       
def pagina_1(driver): #l:50 (pagina_1)
    locator_value = '//*[@name="userMainFrame"]'
    locator_type = 'xpath'
    
    if existe_elemento(driver, locator_value, locator_type):
        user_main_frame =  acessar_elemento(driver, locator_value, locator_type)
        driver.switch_to.frame(user_main_frame)
        
        if existe_elemento(driver, 'container'):
            container = acessar_elemento(driver, 'container')
            # driver.switch_to.frame(container)
            
            if existe_elemento(container, 'content'):
                content = acessar_elemento(driver, 'content')
                # driver.switch_to.frame(content)
                
                if existe_elemento(content, 'mesaAnalistaForm'):
                    form = acessar_elemento(driver, 'mesaAnalistaForm')
                    # driver.switch_to.frame(form)
        
                    while elemento_por_texto_em_lista_by_tag(form, 'h3', 'Mesa do(a) Analista Judiciário') is None:
                        logger.info('Espera Página de Mesa do Analista Judiciário')
                        time.sleep(0.5)
                        
                    # ACESSA ABA OUTROS CUMPRIMENTOS
                    return acessar_aba_outros_cumprimentos(driver)
        
            

def acessar_aba_outros_cumprimentos(driver):
    """
        Método pagina_1: robo clóvis
        Acessa a aba outros cumprimentos, procura pelo cumprimento Madado e se existir clica no link da coluna para expedir (número de mandados)
    """
    locator_value = '//*[@name="tabOutrosCumprimentos"]'
    locator_type = 'xpath'
    
    if existe_elemento(driver, locator_value, locator_type):
        tab_outros_cumprimentos = acessar_elemento(driver, locator_value, locator_type)
        tab_outros_cumprimentos.click()
        
        tabela = buscar_tabela_por_texto(driver, 'Para Expedir', nao_incluso='Outros Cumprimentos') 
        linha_tabela = elemento_por_texto_em_lista_by_tag(tabela, 'tr', 'Mandado') #l:66 (TaskIntimarPessoalmente_SEEU_011.py)
        
        locator_value = 'td'
        locator_type = 'tag'
        if existe_elemento(linha_tabela, locator_value, locator_type):
            colunas = {
                'para_expedir': 2,
                'para_assinar': 3,
                'com_urgencia': 4,
                'devolvido_pelo_juiz': 5,
                'decurso_de_prazo': 6 
            }
            dados_tabela = acessar_elementos(linha_tabela, locator_value, locator_type) #l:67 (TaskIntimarPessoalmente_SEEU_011.py)
            
            driver = dados_tabela[colunas['para_expedir']]
            locator_value = 'a'
            locator_type = 'tag'
            if existe_elemento(driver, locator_value, locator_type):
                tag_a = acessar_elementos(driver, locator_value, locator_type)
                tag_a_link = tag_a[0] #l:69 (TaskIntimarPessoalmente_SEEU_011.py)
                quantidade_madados = int(tag_a_link.text)
                if quantidade_madados > 0:
                    tag_a_link.click() #l:72 (TaskIntimarPessoalmente_SEEU_011.py)
                return quantidade_madados
                
                
 
        
def buscar_tabela_por_texto(driver, texto, id=False, repete=False, completo=False, nao_incluso=None): #l:285 (Metodos.py)
    logger.info(f'buscar_tabela_por_texto - {texto}')
    controlar_tempo_espera(True)
    repete_interno = True
    
    while repete_interno:
        time.sleep(0.1)
        identificacao_erros(driver)
        controlar_tempo_espera(300)
        repete_interno = repete
        # tabelas = driver.find_elements(by=By.TAG_NAME, value='table')
        locator_value = 'table'
        locator_type = 'tag'
        if existe_elemento(driver, locator_value, locator_type):
            tabelas = acessar_elementos(driver, locator_value, locator_type)
            for index, tabela in enumerate(tabelas):
                if "Traceback (most recent call last)" not in tabela.text:
                    continua = True
                    if nao_incluso is not None:
                        continua = False
                        if nao_incluso not in tabela.text:
                            continua = True
                    if texto in tabela.text and continua:
                        if completo:
                            return index, tabela, tabelas
                        if id:
                            return index
                        return tabela
    return None
        
    


def controlar_tempo_espera(inicio=False, max=600): #l:199 (Metodos.py)
        if inicio:
            tempo_espera = 0
        else:
            tempo_espera += 1
            if tempo_espera % 60 == 0:
                print("Mais 60", tempo_espera)
        if tempo_espera >= max:
            print("Excedeu o tempo")
            raise Exception("Excedeu o tempo")
        # if trata_solicitacao is not None:
        #     self.trata_solicitacao()
            
            
def identificacao_erros(driver): #l:77 (Metodos.py)
    locator_value = '//*[@id="pageBody"]/ul/li'
    locator_type = 'xpath'
    
    # if existe_elemento(driver, locator_value, locator_type):
    if _check_exists_by_xpath(driver, locator_value): #
        if 'Erro inesperado, por favor tente novamente' in \
            driver.find_element(by=By.XPATH, value=locator_value).text:
            url = driver.current_url
            driver.get(url)
            logger.info("Retornando ao ponto inicial devido a erros")
            raise Exception("Retornando ao ponto inicial devido a erros")        


def _check_exists_by_xpath(driver, xpath): #l:53 (Metodos.py)
    try:
        driver.find_element(by=By.XPATH, value=xpath)
    except NoSuchElementException:
        return False
    return True


def elemento_por_texto_em_lista_by_tag(driver, tag, texto, repete=False, nao_incluso=None): #l:56
    print("elemento_por_texto_em_lista_by_tag -", texto)
    repete_interno = True
    while repete_interno:
        repete_interno = repete
        # elementos = driver.find_elements(by=By.TAG_NAME, value=tag)
        if existe_elemento(driver, tag, 'tag'):
            elementos = acessar_elementos(driver, tag, 'tag')
            for elemento in elementos:
                continua = True
                if nao_incluso is not None: 
                    continua = False 
                    if nao_incluso not in elemento.text:
                        continua = True
                if texto in elemento.text and continua \
                    and "Traceback (most recent call last)" not in elemento.text:
                    return elemento
        # if self.trata_solicitacao is not None:
        #     self.trata_solicitacao()
    return None 

         
def pagina_2(driver):
    """
      Acessa os madados no na aba de compridos e para cada mandado clica na coluna "Pré-Análise" e em "[Analisar]"  
    """
    while elemento_por_texto_em_lista_by_tag(driver, "h3", "Mandados") is None:
        print("Espera Página de Mandados")
        time.sleep(0.5)

    table = acessar_elemento(driver, '//*[@id="cumprimentoCartorioMandadoForm"]/table[1]/tbody', 'xpath', 20) #l82: (TaskIntimarPessoalmente_SEEU_011.py) 
    tr = table.find_elements(by=By.TAG_NAME, value="tr")
    td = tr[0].find_elements(by=By.TAG_NAME, value="td")
    processo = td[5].text 
    td[15].find_elements(by=By.TAG_NAME, value="td")[1].click() # //*[@id="cumprimentoCartorioMandadoForm"]/table[4]/tbody/tr[1]/td[16]/table/tbody/tr/td[2]
    time.sleep(1.5)
    return processo   
            
            
def pagina_3(driver):
    """
        Acessa a página de Pré-Análise, preenche as informações Tipo do Arquivo, Modelo e clica no botão "Digitar Texto"
    """
    while elemento_por_texto_em_lista_by_tag(driver, "h4", "Arquivos") is None:
            print("Espera Página de Arquivos")
            time.sleep(0.5)

    file_type_select = acessar_elemento(driver, '//*[@id="descricaoTipoArquivo"]', 'xpath')
    file_type_select.send_keys('Mandado')
    type_opcao = acessar_elemento(driver, '//*[@id="101"]', 'xpath')
    type_opcao.click()
    
    file_type_model = acessar_elemento(driver, '//*[@id="descricaoModelo"]', 'xpath')
    modelo = "(Deusilene dos Santos Souza - Analista Judiciário ) - MANDADO - LIVRAMENTO CONDICIOANL" #l:21 (config.xml)
    modelo_split = modelo.split(") - ")[-1]
    file_type_model.send_keys(modelo_split)
    time.sleep(1.5)
    type_model = driver.find_element(By.XPATH, "//li[contains(text(), '"+modelo_split+"')]")
    type_model.click()
    
    print("Clique no Digitar Texto")
    type_text = acessar_elemento(driver, '//*[@id="digitarButton"]', 'xpath')
    type_text.click()
    print("Fim clique no Digitar Texto")
    

def pagina_4(driver):
    '''
        Entra no detalhe da pré-análise e salva os dados do editor.
    '''
    while elemento_por_texto_em_lista_by_tag(driver, "h3", "Digitar Documento") is None:
        print("Espera Página de Digitar Documento")
        time.sleep(0.5)

    if existe_elemento(driver, '//*[@id="submitButton"]', 'xpath'):
        continue_button = acessar_elemento(driver, '//*[@id="submitButton"]', 'xpath')
        continue_button.click()

        while elemento_por_texto_em_lista_by_tag(driver, "h3", "Documento") is None:
            print("Espera Página de Documento")
            time.sleep(0.5)

        if existe_elemento(driver, '//*[@id="submitButton"]', 'xpath'):
            save_button = acessar_elemento(driver, '//*[@id="submitButton"]', 'xpath')
            save_button.click()
    
            