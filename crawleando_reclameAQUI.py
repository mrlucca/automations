"""
	@outor: mrlucca

"""

#importando bibliotecas necessarias do selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from time import sleep


class Reclame_aqui:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://www.reclameaqui.com.br/empresa/magazine-luiza-loja-fisica/lista-reclamacoes/'

        #iniciando a url principal de extração de dados 
    def Start_browser(self):
        self.driver.get(self.url)

    def Data_box(self):
        #pegando a pag da web e estruturando em um objeto bs de formato html
        dados_pag = self.driver.page_source
        page_web = bs(dados_pag, 'html.parser')

        #pegando os links da pag de reclamações
        boxes_links = page_web.find_all('a',{'class': 'link-complain-id-complains'})
        href_links = [box.get('href') for box in boxes_links]
        return href_links




#iniciando o bot
driver = webdriver.Chrome()
driver.implicitly_wait(10)
bot = Reclame_aqui(driver)
bot.Start_browser()
bot.Data_box()

#montado os links do site para os box de reclamação individual
links_boxes_reclamacao = bot.Data_box()
base_url = 'https://www.reclameaqui.com.br/'
links_montados = [f'{base_url}{link}' for link in links_boxes_reclamacao] #list comprehension das urls, concatena a url principal do reclame aqui
                                                                          #com as urls pegas na pag principal de reclamação da magazine

#navegando sobre as paginas dos links montados
def varredor():
    for link in links_montados:
        #laço para entrar em todas as paginas de reclamação da pag principal
        driver.get(link)
        sleep(5)
        dados_pag = bs(driver.page_source, 'html.parser')
        title = dados_pag.find('h1', {'class': 'ng-binding'}).text
        cidade = dados_pag.find('li', {'class': 'ng-binding'}).text
        id = dados_pag.find('li', {'class':'ng-scope'}).text
        paragrafo = dados_pag.find('div', {'class':'complain-body'}).text
        print(''' ===============================================+++++++++++++===========================================================
TITULO: {}
CIDADE: {}                    ID: {}

RECORRENCIA: {}
                    '''.format(title, cidade, id, paragrafo))




varredor()
