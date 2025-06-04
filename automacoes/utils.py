from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

LOCATOR_MAP = {
    'id': By.ID,
    'class': By.CLASS_NAME,
    'xpath': By.XPATH,
    'css': By.CSS_SELECTOR,
    'tag': By.TAG_NAME,
    'name': By.NAME,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT
}

def acessar_elemento_visivel(driver, locator_value, locator_type="id", timeout=15):
    try:
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((LOCATOR_MAP[locator_type.lower()], locator_value))
        )
        debug_elemento(elemento)
        
        return elemento
    except TimeoutException:
        raise TimeoutException(f"Elemento não encontrado após {timeout} segundos. "
                             f"Localizador: {locator_type}='{locator_value}'")
        

def acessar_elementos_visiveis(driver, locator_value, locator_type="id", timeout=15):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((LOCATOR_MAP[locator_type.lower()], locator_value))
        )
        # debug_elemento(elemento) TODO Implementar o depurador para listas
        
        # return elemento
    except TimeoutException:
        raise TimeoutException(f"Elementos não encontrados após {timeout} segundos. "
                             f"Localizador: {locator_type}='{locator_value}'")
        
        
def acessar_elemento_clicavel(driver, locator_value, locator_type="id", timeout=60):
    try:
        elemento = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((LOCATOR_MAP[locator_type.lower()], locator_value))
        )
        debug_elemento(elemento)
        
        return elemento
    except TimeoutException:
        raise TimeoutException(f"Elemento não clicável após {timeout} segundos. "
                             f"Localizador: {locator_type}='{locator_value}'")
        
        
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