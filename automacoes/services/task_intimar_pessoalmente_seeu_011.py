from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException

from automacoes.utils import acessar_elemento_visivel, acessar_elemento_clicavel, acessar_elementos_visiveis, existe_elemento

import os.path
import time
import logging
import re

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

corporativo_login = os.environ.get('CORPORATIVO_LOGIN')
corporativo_pass = os.environ.get('CORPORATIVO_PASS')

class TaskIntimarPessoalmente:
    
    def __configurar_driver(self):
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--start-maximized")
        options.add_argument("--dissable-cache")
        
        # Disable cache
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-cache")
        options.add_argument("--disable-disk-cache")
        options.add_argument("--disable-memory-cache")
        options.add_argument("--disable-offline-load-stale-cache")
        options.add_argument("--disk-cache-size=0")
        
        # Additional cache-related arguments
        options.add_argument("--aggressive-cache-discard")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        
        return webdriver.Chrome(
                service=Service(os.path.expanduser('~/chromedriver')),
                options=options,
            )
        
    def iniciar_automacao(self):
        logger.info(f'Inciando Automação Intimar Pessoalmente')
        self.loginSeeu()
        
    
    def loginSeeu(self):
        driver = self.__configurar_driver()
        driver.set_page_load_timeout(60)
        driver.implicitly_wait(15)
        driver.get('https://seeuintegra.pje.jus.br/seeu/')
        
        try:
            iframe = acessar_elemento_visivel(driver, 'mainFrame')
            driver.switch_to.frame(iframe)
            
            janela_original = driver.current_window_handle
            acessar_elemento_clicavel(driver, "btn-login-corporativo").click()
            
            corporaivo = WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
            if corporaivo:
                todas_janelas = driver.window_handles
                novas_abas = [ janela for janela in todas_janelas if janela != janela_original]
                
                if novas_abas:
                    nova_aba = novas_abas[0]
                    
                    if not isinstance(nova_aba, str):
                        nova_aba = str(nova_aba)
                    driver.switch_to.window(str(nova_aba))
                    
                    acessar_elemento_visivel(driver, 'username').send_keys(corporativo_login)
                    acessar_elemento_visivel(driver, 'password').send_keys(corporativo_pass)
                    acessar_elemento_clicavel(driver, 'kc-login').click()
                    
                    janela_atual_seeu = driver.switch_to.window(janela_original)
                    todas_janelas_atualis = driver.window_handles
                    novas_abas_atuais = [ janela_atual for janela_atual in todas_janelas_atualis if janela_atual != janela_atual_seeu]
                    
                    if novas_abas_atuais:
                        nova_aba_atual = novas_abas_atuais[0]
                        
                        if not isinstance(nova_aba_atual, str):
                            nova_aba_atual = str(nova_aba_atual)
                            
                        driver.switch_to.window(nova_aba_atual)
                    
                        logger.info(f'Url atual: {driver.current_url}')
                        logger.info('Etapa de autenticacao finalizada')
                        
                        self.continua_seeu_apos_login(driver)
        except Exception as e:
            print(f"Erro ao acessar elementos na nova aba: {e}")
            driver.close()
            
            
    def elemento_por_texto_em_lista_by_tag(self, driver, tag, texto, repete=False, nao_incluso=None): #l:56 TODO Refatorar método para melhorar performace
        print("elemento_por_texto_em_lista_by_tag -", texto)
        repete_interno = True
        while repete_interno:
            repete_interno = repete
            elementos = acessar_elementos_visiveis(driver, tag, 'tag')
            if elementos:
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
    
    
    def __controlar_tempo_espera(self, inicio=False, max=600): #l:199 (Metodos.py)
        tempo_espera = 0
        if not inicio:
            tempo_espera += 1
            if tempo_espera % 60 == 0:
                print("Mais 60", tempo_espera)
        if tempo_espera >= max:
            print("Excedeu o tempo")
            raise Exception("Excedeu o tempo")
        # if trata_solicitacao is not None:
        #     self.trata_solicitacao()
      
      
    def __identificacao_erros(self, driver): #l:77 (Metodos.py)
        locator_value = '//*[@id="pageBody"]/ul/li'
        locator_type = 'xpath'
        
        # if existe_elemento(driver, locator_value, locator_type):
        if self._check_exists_by_xpath(driver, locator_value): #
            if 'Erro inesperado, por favor tente novamente' in \
                driver.find_element(by=By.XPATH, value=locator_value).text:
                url = driver.current_url
                driver.get(url)
                logger.info("Retornando ao ponto inicial devido a erros")
                raise Exception("Retornando ao ponto inicial devido a erros")        


    def _check_exists_by_xpath(self, driver, xpath): #l:53 (Metodos.py)
        try:
            driver.find_element(by=By.XPATH, value=xpath)
        except NoSuchElementException:
            return False
        return True  
    
    
    def __buscar_tabela_por_texto(self, driver, texto, id=False, repete=False, completo=False, nao_incluso=None): #l:285 (Metodos.py)
        print("buscar_tabela_por_texto -", texto)
        self.__controlar_tempo_espera(True)
        repete_interno = True
        while repete_interno:
            time.sleep(0.1)
            self.__identificacao_erros(driver)
            self.__controlar_tempo_espera(max=300)
            repete_interno = repete
            tabelas = driver.find_elements(by=By.TAG_NAME, value='table')
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
    
    
    def __filtrar_por_varas_excecucoes_penais(self, nome_vara):
        paradrao_explicito =  r'\b(Execução|Execuções|Penal|Penais)\b'
        
        return re.findall(paradrao_explicito, nome_vara, re.IGNORECASE)       
            
            
    def acessar_vara(self, driver, elementos): 
        for elemento in elementos:
            acessar_elemento_clicavel(elemento, 'a', 'tag', timeout=60).click()
            # logger.info(f'Acessando a vara: {debug_elemento(elemento)}')
            
            driver.switch_to.default_content()
            
            driver.switch_to.frame(acessar_elemento_visivel(driver, 'mainFrame', timeout=60))
            logger.info('Recarregar os elementos na tela de varas')
            
            # Abre o primeiro shadowroot
            if existe_elemento(driver, '#header', 'css'):
                shadow_root_01 = acessar_elemento_visivel(driver, '#header', 'css', timeout=60).shadow_root
                logger.info('Abre novamente o shadow root')
                # Elemento de texto começa a partir do terceiro filho
                count = 3
            
                try:
                    while True:
                        # Localiza a vara a ser trocada
                        nome_vara = str(shadow_root_01.find_element(By.CSS_SELECTOR,
                            'div.flex-grow seeu-dropdown seeu-menu-item:nth-child(' + str(count) + ')').text).strip()
                        if nome_vara:
                            filtro_vara = self.__filtrar_por_varas_excecucoes_penais(nome_vara)
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
      
      
    def acessar_lista_atuacao(self, driver): #l:526 (ExecuteAlteraVara - TaskIntimarPessoalmente_SEEU_011)
        locator_value = 'listaAreavara'
        acessar_elemento_visivel(driver, locator_value, timeout=60)
        time.sleep(0.5)
        # if el_lista_area_vara:
        locator_value = f"#{locator_value} li"
        elementos = acessar_elementos_visiveis(driver, locator_value, 'css')
        result = self.acessar_vara(driver, elementos) # l:528 (TaskIntimarPessoalmente_SEEU_011.PY)
        
        if not result:
            logger.info('Nao foi possivel alterar a vara')
            logger.info('Finalizando robo')
            
            return result
        
        return driver      
    
    

    
    
    def continua_seeu_apos_login(self, driver):
        try:
            iframe = acessar_elemento_visivel(driver, 'mainFrame')
            driver.switch_to.frame(iframe)
            driver = self.acessar_lista_atuacao(driver) #l:619 (method: automacao) (TaskIntimarPessoalmente_SEEU_11)
            
            if not driver:
                raise Exception('Falha ao mudar de vara')
            
            
            
            continuacao = True
            while continuacao:
                continuacao = False
                time.sleep(1)
                
                self.acessar_mesa_analista_tab_inicio(driver) #l:633, pagina_1 (TaskIntimarPessoalmente_SEEU_11)
                time.sleep(1)
                self.acessar_mandados_pre_analise(driver) #l640, pagina_2 (TaskIntimarPessoalmente_SEEU_11.py)
                time.sleep(1)
                # TODO Aqui entraria a parte do log e geração de arquivo em excell
                
                try:
                    self.acessar_tab_pre_analise_e_preencher_campos(driver) #l:649, pagina_3 (TaskIntimarPessoalmente_SEEU_11)
                except Exception as e:
                    # TODO Caso ocorra excessão enviar error para o log.
                    pass
                
                # time.sleep(1)
                try:
                    self.acessar_editor_documento_salvar_dados(driver) #l:113, pagina_4 (TaskIntimarPessoalmente_SEEU_11.py)
                    logger.info(f'Finalizou pagina_4')
                except Exception as e:
                    # TODO Caso ocorra excessão enviar error para o log.
                    pass
                time.sleep(1)
                try:
                    self.acessar_tela_arquivo(driver) # l:129 (TaskIntimarPessoalmente_SEEU_011.py)
                    logger.info(f'Finalizou pagina_5')
                except Exception as e:
                    pass
                try:
                    self.acessar_processo_e_preenchar_dados(driver) #l:147 (TaskIntimarPessoalmente_SEEU_011.py)
                    logger.info(f'acessar_processo_e_preenchar_dados')
                except Exception as e:
                    pass
                try:
                    self.abrir_modal_selecao_documentos(driver) #l170 (TaskIntimarPessoalmente_SEEU_011.py)
                    logger.info(f'Finalizou pagina_7')
                except Exception as e:
                    pass
                time.sleep(1)
                try:
                    self.selecionar_documentos_outras_decisoes(driver) #l:715, pagina_8(TaskIntimarPessoalmente_SEEU_011.py)
                    logger.info(f'Finalizou pagina_8')
                except Exception as e:
                    pass
                time.sleep(1)
                try:
                    self.postegar_assinatura_arquivo(driver) #l:728, pagina_9(TaskIntimarPessoalmente_SEEU_011.py)
                    logger.info(f'Finalizou pagina_9')
                except Exception as e:
                    pass

                
        except Exception as e:
            logger.error(e)
            logger.info('Ocorreu uma falha ao autenticar')
        
        logger.info('Acessou SEEU')
        
        time.sleep(2)
        
        
    def acessar_mesa_analista_tab_inicio(self, driver):  #l:50 (pagina_1)
        logger.info('Acessou a mesa do analista') #l:628
        user_main_frame = acessar_elemento_visivel(driver, 'userMainFrame', timeout=60)
        driver.switch_to.frame(user_main_frame)

        el_container = acessar_elemento_visivel(driver, 'container', timeout=60)
        el_content = acessar_elemento_visivel(el_container, 'content')
        mesa_analista_form = acessar_elemento_visivel(el_content, 'mesaAnalistaForm')
        
        while self.elemento_por_texto_em_lista_by_tag(mesa_analista_form, 'h3', 'Mesa do(a) Analista Judiciário') is None:
            logger.info('Espera Página de Mesa do Analista Judiciário')
            time.sleep(0.5)
        
        self.acessar_tab_outros_cumprimentos(driver)
        
        
    def acessar_tab_outros_cumprimentos(self, driver):
        """
            Método pagina_1: robo clóvis
            Acessa a aba outros cumprimentos, procura pelo cumprimento Madado e se existir clica no link da coluna para expedir (número de mandados)
        """
        acessar_elemento_clicavel(driver, '//*[@name="tabOutrosCumprimentos"]', 'xpath').click() #:61, pagina_1 (TaskIntimarPessoalmente_SEEU_011.py)
            
        tabela = self.__buscar_tabela_por_texto(driver, 'Para Expedir', nao_incluso='Outros Cumprimentos') 
        tr = self.elemento_por_texto_em_lista_by_tag(tabela, 'tr', 'Mandado') #l:66 (TaskIntimarPessoalmente_SEEU_011.py)
        
        tds = acessar_elementos_visiveis(tr, 'td', 'tag')
        if tds:
            colunas = {
                'para_expedir': 2,
                'para_assinar': 3,
                'com_urgencia': 4,
                'devolvido_pelo_juiz': 5,
                'decurso_de_prazo': 6 
            }
            
            driver = tds[colunas['para_expedir']]
            
            el_tag_a = acessar_elemento_clicavel(driver, 'a', 'tag', timeout=15)
            quantidade_madados_expedir = int(el_tag_a.text)
            
            if quantidade_madados_expedir > 0:
                logger.info(f'Quantidade de mandados para expedir: {quantidade_madados_expedir}')
                el_tag_a.click() #l:72 (TaskIntimarPessoalmente_SEEU_011.py)
            else:
                raise Exception('Nenhum mandado para expedir')
            
            
    def acessar_mandados_pre_analise(self, driver): #l:76, pagina_2(TaskIntimarPassoalmente_SEEU_011.py)
        """
        Acessa os madados no na aba de compridos e para cada mandado clica na coluna "Pré-Análise" e em "[Analisar]"  
        """
        while self.elemento_por_texto_em_lista_by_tag(driver, "h3", "Mandados") is None:
            print("Espera Página de Mandados")
            time.sleep(0.5)

        el_table = acessar_elemento_visivel(driver, '//*[@id="cumprimentoCartorioMandadoForm"]/table[1]/tbody', 'xpath') #l82: (TaskIntimarPessoalmente_SEEU_011.py) 
        el_tr = acessar_elemento_visivel(el_table, 'tr', 'tag')
        el_td = acessar_elementos_visiveis(el_tr, 'td', 'tag')
        processo = el_td[5].text 
        if processo:
            logger.info(f'Finalizou pagina_2, processo: {processo}')
            el_td[15].find_elements(by=By.TAG_NAME, value="td")[1].click() # //*[@id="cumprimentoCartorioMandadoForm"]/table[4]/tbody/tr[1]/td[16]/table/tbody/tr/td[2]
            
            
    def acessar_tab_pre_analise_e_preencher_campos(self, driver):
        """
            Acessa a página de Pré-Análise, preenche as informações Tipo do Arquivo, Modelo e clica no botão "Digitar Texto"
        """
        while self.elemento_por_texto_em_lista_by_tag(driver, "h4", "Arquivos") is None:
            print("Espera Página de Arquivos")
            time.sleep(0.5)

        acessar_elemento_visivel(driver, '//*[@id="descricaoTipoArquivo"]', 'xpath').send_keys('Mandado')
        acessar_elemento_clicavel(driver, '//*[@id="101"]', 'xpath').click()
        
        modelo = "(Deusilene dos Santos Souza - Analista Judiciário ) - MANDADO - LIVRAMENTO CONDICIOANL" #l:21 (config.xml)
        modelo_split = modelo.split(") - ")[-1]
        
        acessar_elemento_clicavel(driver, '//*[@id="descricaoModelo"]', 'xpath').send_keys(modelo_split)
        # type_model = driver.find_element(By.XPATH, "//li[contains(text(), '"+modelo_split+"')]")
        # type_model.click()
        acessar_elemento_clicavel(driver, "//li[contains(text(), '"+modelo_split+"')]", 'xpath').click()
        
        print("Clique no Digitar Texto")
        type_text = acessar_elemento_visivel(driver, '//*[@id="digitarButton"]', 'xpath')
        type_text.click()
        print("Fim clique no Digitar Texto")
        
        
    def acessar_editor_documento_salvar_dados(self, driver): #TODO refatora condicionais
      
        while self.elemento_por_texto_em_lista_by_tag(driver, "h3", "Digitar Documento") is None:
            print("Espera Página de Digitar Documento")
            time.sleep(0.5)

        acessar_elemento_clicavel(driver, '//*[@id="submitButton"]', 'xpath').click()
       
        while self.elemento_por_texto_em_lista_by_tag(driver, "h3", "Documento") is None:
            print("Espera Página de Documento")
            time.sleep(0.5)

        acessar_elemento_clicavel(driver, '//*[@id="submitButton"]', 'xpath').click()

    
    def acessar_tela_arquivo(self, driver):
        while self.elemento_por_texto_em_lista_by_tag(driver, "h4", "Arquivos") is None:
            print("Espera Página de Arquivos")
            time.sleep(0.5)
            
        acessar_elemento_clicavel(driver, '//*[@id="finishButton"]', 'xpath').click()

        while self.elemento_por_texto_em_lista_by_tag(driver, "h4", "Arquivos") is None:
            print("Espera Página de Arquivos")
            time.sleep(0.5)
            
        acessar_elemento_clicavel(driver, '//input[@id="editButton" and @value="Alterar"]', 'xpath').click()

        time.sleep(1)
        
        
    def acessar_processo_e_preenchar_dados(self, driver): 
        acessar_elemento_clicavel(driver, '//*[@id="cumprimentoCartorioMandadoForm"]/fieldset/table[1]/tbody/tr[10]/td[2]/label/input[1]', 'xpath').click()
        acessar_elemento_visivel(driver, '//*[@id="codCustasMandado"]', 'xpath').send_keys('c')
        acessar_elemento_clicavel(driver, '//*[@id="cumprimentoCartorioMandadoForm"]/fieldset/table[1]/tbody/tr[6]/td[2]/label[1]/input', 'xpath').click() 
        acessar_elemento_clicavel(driver, '//*[@id="cumprimentoCartorioMandadoForm"]/fieldset/table[1]/tbody/tr[12]/td[2]/label[2]/input', 'xpath').click()
        acessar_elemento_clicavel(driver, '//*[@id="rowAssinadoPorJuiz"]/td[2]/label[2]/input', 'xpath').click()
        
        logger.info(f'Acessando id: prazoOficialJustica')
        probation_officer_term = acessar_elemento_visivel(driver, '//*[@id="prazoOficialJustica"]', 'xpath')
        
        for i in range(10): 
            probation_officer_term.send_keys(Keys.BACK_SPACE)
        probation_officer_term.send_keys('15')

        time.sleep(0.5)

        acessar_elemento_clicavel(driver, '//*[@id="saveButton"]', 'xpath').click()
        
        
    def abrir_modal_selecao_documentos(self, driver): # l: 702 (TaskIntimarPessoalmente_SEEU_011)
        while self.elemento_por_texto_em_lista_by_tag(driver, "h4", "Arquivos") is None:
            logger.info("Espera Página de Arquivos")
            time.sleep(0.5)

        acessar_elemento_clicavel(driver, '//input[@id="editButton" and @value="Adicionar"]', 'xpath').click()
        time.sleep(2)
        
        
    def selecionar_documentos_outras_decisoes(self, driver):
        pop_up_frame = acessar_elemento_visivel(driver, '//iframe[@frameborder="0"]', 'xpath', timeout=60)
        pop_up_name = pop_up_frame.get_attribute('name')
        pop_up_name = "_".join(pop_up_name.split("_")[:-1])

        driver.switch_to.frame(pop_up_frame)
        
        table = acessar_elemento_visivel(driver, '//*[@id="cumprimentoCartorioMandadoForm"]/table[1]/tbody', 'xpath')
        trs = acessar_elementos_visiveis(table, 'tr', 'tag')
        funcionou, opcao, indice = self.selecionar_anexo(trs)

        if funcionou:
            inputs_check = acessar_elementos_visiveis(trs[indice+2], 'input', 'tag')
            inputs_check[0].click()
            time.sleep(0.5)
            acessar_elemento_clicavel(driver, '//*[@id="selectButton"]', 'xpath').click()
        else:
            mensagem = "Não foi possível encontrar checkbox de um documento válido. Realize o procedimento adequado para esse caso."
            logger.info("Não foi possível encontrar checkbox de um documento válido. Aguardando o usuário realizar procedimento adequado.")
            logger.warning(mensagem)
        
        # while self.elemento_por_texto_em_lista_by_tag(driver, "h3", "Seleção de Documentos") is not None:
        #     logger.info("Espera Sair de Seleção de Documentos")
        #     time.sleep(0.5)

        return opcao
        
        
    def selecionar_anexo(self, trs):
        despachos = ["Assistência Judiciária Gratuita",
                        "Conflito de Competência", 
                        "Exceção da Verdade", 
                        "Exceção de Incompetência, suspeição ou Impedimento",
                        "Incidente de Insanidade Mental", 
                        "Expedição de alvará de levantamento",
                        "Julgamento em Diligência",
                        "Mero expediente",
                        "Ordenação de entrega de autos",
                        "Requisição de Informações"]
        
        decisoes = ["A depender do julgamento de outra causa, de outro juízo ou declaração incidente",
                    "Força maior",
                    "Livramento Condicional", 
                    "Morte ou perda da capacidade", 
                    "Por decisão judicial", 
                    "Réu revel citado por edital", 
                    "Suspensão Condicional do Processo",
                    "Antecipação de tutela", 
                    "Comutação da pena", 
                    "Detração/Remição da Pena", 
                    "Direito de visita", 
                    "Indulto", 
                    "Liberdade provisória", 
                    "Liminar", 
                    "Livramento Condicional", 
                    "Medida protetiva", 
                    "Permissão de saída", 
                    "Prisão Domiciliar", 
                    "Progressão de regime", 
                    "Suspensão Condicional da Pena",
                    "Arquivamento", 
                    "Bloqueio/penhora on line", 
                    "Demonstração de existência de repercussão geral e manifestação sobre a questão constitucional", 
                    "Determinação de arquivamento de procedimentos investigatórios", 
                    "Devolução da carta rogatória ao juízo rogante", 
                    "Devolução dos autos à origem", 
                    "Distribuição", 
                    "Juízo provisório para medidas urgentes", 
                    "Quebra de sigilo bancário", 
                    "Quebra de sigilo fiscal", 
                    "Quebra de sigilo telemático",
                    "Regressão de Medida Sócio-Educativa",
                    "Regressão de Regime",
                    "Assistência judiciária gratuita", 
                    "Liberdade Provisória", 
                    "Liminar", 
                    "Medida protetiva",
                    "Assistência Judiciária Gratuita", 
                    "Decisão anterior", 
                    "Detração/Remição", 
                    "Liminar", 
                    "Livramento Condicional", 
                    "Medida protetiva", 
                    "Medida protetiva determinada por autoridade policia", 
                    "Prisão", 
                    "Revogação da Suspensão do Processo", 
                    "Suspensão Condicional da Pena", 
                    "Cancelamento da distribuição",
                    "Com efeito suspensivo", 
                    "Sem efeito suspensivo", 
                    "Decisão de Saneamento e de Organização", 
                    "Decisão Interlocutória de Mérito", 
                    "deferimento",
                    "Denúncia", 
                    "Exceção de Impedimento ou Suspeição", 
                    "Exceção de incompetência",
                    "Desistência de Recurso", 
                    "Medida protetiva determinada por autoridade policial", 
                    "Domiciliar", 
                    "Embargos", 
                    "Reclamação", 
                    "Impedimento", 
                    "Incompetência", 
                    "Remição", 
                    "Suspeição", 
                    "Impedimento ou Suspeição", 
                    "Incompetência",  
                    "Inclusão em Regime Disciplinar Diferenciado", 
                    "pagamento", 
                    "Recambiamento de Preso", 
                    "Saída Temporária", 
                    "Trabalho Externo", 
                    "Transferência da Execução da Pena", 
                    "Transferência para outro Estabelecimento Penal", 
                    "Indeferimento", 
                    "Liminar", 
                    "Medida protetiva", 
                    "Liminar Prejudicada", 
                    "Outras Decisões", 
                    "Pena / Medida", 
                    "Preventiva", 
                    "Temporária", 
                    "Prorrogação de cumprimento de pena/medida de segurança", 
                    "Provisória",
                    "Recurso", "Reforma de decisão anterior", 
                    "Relaxamento do Flagrante", 
                    "Suscitação de Conflito de Competência", 
                    "Unificação e Soma de Penas",
                    "Unificadas e Somadas as Penas"]
        
        despachos = [x.upper() for x in despachos]
        decisoes = [x.upper() for x in decisoes]

        funcionou = False
        opcao = None
        indice = 0
        for indice, tr in enumerate(trs):
            tag_b = tr.find_elements(by=By.TAG_NAME, value="b")
            if len(tag_b)>0:
                tag_b = tag_b[0]
                for despacho in despachos:
                    if despacho in tag_b.text.upper():
                        funcionou = True
                        opcao = despacho
                        # if get_elements_by_tag(trs[indice+2], "input") is not None:
                        acessar_elemento_visivel(trs[indice+2], 'input', 'tag')
                        # if existe_elemento(trs[indice+2], 'input', 'tag'):
                        return funcionou, "Despacho: "+opcao, indice
                for decisao in decisoes:
                    if decisao in tag_b.text.upper():
                        funcionou = True    
                        opcao = decisao
                        # if get_elements_by_tag(trs[indice+2], "input") is not None:
                        acessar_elemento_visivel(trs[indice+2], 'input', 'tag')
                        # if existe_elemento(trs[indice+2], 'input', 'tag'):
                        return funcionou, "Decisão: "+opcao, indice
        return funcionou, "Não Encontrado", indice
    
    
    def postegar_assinatura_arquivo(self, driver):
        driver.switch_to.default_content() #;:339 (TaskIntimarPessoalmente_SEEU_011.py)
        
        main_frame = acessar_elemento_visivel(driver, '//*[@name="mainFrame"]', 'xpath')
        driver.switch_to.frame(main_frame)
        
        user_main_frame =  acessar_elemento_visivel(driver, '//*[@name="userMainFrame"]', 'xpath')
        driver.switch_to.frame(user_main_frame)
        
        # while self.elemento_por_texto_em_lista_by_tag(driver, "h4", "Arquivos") is None:
        #     print("Espera Página de Arquivos")
        #     time.sleep(0.5)

        # time.sleep(1)
        
        acessar_elemento_clicavel(driver, '//*[@id="postergarButton" and @value="Postergar Assinatura"]', 'xpath').click()
