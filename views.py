import threading
import tkinter as tk
from tkinter import messagebox

from django import shortcuts
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def index(request):
    return shortcuts.render(request, 'index.html', {
        'title': 'Bem vindo!!'
    })


def selenium(request):
    t = threading.Thread(target=tarefa)
    t.daemon = True
    t.start()
    return index(request)


def tarefa():
    options = Options()

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    driver.implicitly_wait(3)
    driver.get('https://demoqa.com/forms')
    driver.find_element(
        By.XPATH,
        '/html/body/div[2]/div/div/div/div[1]/div/div/div[2]/div/ul/li/span'
    ).click()

    driver.find_element(By.ID, 'firstName').send_keys('Igor')
    driver.find_element(By.ID, 'lastName').send_keys('Carvalho')
    driver.find_element(By.ID, 'userEmail').send_keys('igor.carvalho@tjpa.jus.br')

    driver.find_element(By.CSS_SELECTOR, 'div.custom-radio:nth-child(3) > label:nth-child(2)').click()

    data_nascimento = driver.find_element(By.ID, 'dateOfBirthInput')
    driver.execute_script("arguments[0].select();", data_nascimento)
    data_nascimento.send_keys('30 Sep 1983')
    data_nascimento.send_keys(Keys.ENTER)

    driver.find_element(By.ID, 'userNumber').send_keys('91996418559')
    subjects = driver.find_element(By.ID, 'subjectsInput')
    subjects.send_keys('computer')
    subjects.send_keys(Keys.ENTER)

    driver.find_element(By.CSS_SELECTOR, 'div.custom-checkbox:nth-child(1) > label:nth-child(2)').click()
    driver.execute_script("document.getElementById('submit').click()")

    show_dialog_and_wait('Automação finalizada')

    driver.find_element(By.ID, 'closeLargeModal').click()
    driver.quit()


def show_dialog_and_wait(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Informação", message)
    root.destroy()
