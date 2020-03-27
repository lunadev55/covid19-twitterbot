
# PIP:
    # pip install requests2
    # pip install pandas
    # pip install lxml
    # pip install beautifulsoup4
    # pip install selenium

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

from datetime import datetime

import tweepy as tp
import time
import os

# credentials to login to twitter api
# you should create a twitter developer account to have access ...
# ... to your keys and them fill them in down below
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

# login to twitter account api
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)

while (True):    
    url = 'https://www.worldometers.info/coronavirus/'

    option = Options()
    option.headless = True
    driver = webdriver.Firefox(options=option)
    driver.get(url)

    time.sleep(10)

    # get the 3 maincounter-number div class in which have the content for
    # cases, deaths and recovered
    elem = driver.find_elements_by_xpath("//div[@class='maincounter-number']//span")

    cases = elem[0].get_attribute('innerHTML')
    deaths = elem[1].get_attribute('innerHTML')
    recoveres = elem[2].get_attribute('innerHTML')

    driver.quit()

    api.update_status('CONTEUDO ATUALIZADO SOBRE O COVID-19\n\n' +
                        'DATA: ' + str(datetime.now()) + '\n\n' +
                        'CASOS NO MUNDO: ' + cases + '\n' +
                        'MORTES: ' + deaths + '\n' +
                        'RECUPERADOS: ' + recoveres + '\n')

    time.sleep(20)




