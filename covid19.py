
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

#credentials to login to twitter api
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

# login to twitter account api
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)

# date and time to Brazilian format
def formatDate(hour):
    day = hour[8:10]
    mon = hour[5:7]
    year = hour[:4]
    full_date = day + '/' + mon + '/' + year

    hours = hour[11:13]
    minutes = hour[14:16]
    full_hours = hours + ':' + minutes

    full_string = ('Data: ' + full_date + '\n' + 
                    'Horario: ' + full_hours)

    return full_string

while (True):    
    url = 'https://www.worldometers.info/coronavirus/'

    option = Options()
    option.headless = True
    driver = webdriver.Firefox(options=option)
    driver.get(url)

    time.sleep(10)

    # get the 3 maincounter-number div class in which have the content for
    # cases, deaths and recovered
    main = driver.find_elements_by_xpath("//div[@class='maincounter-number']//span")

    cases = main[0].get_attribute('innerHTML')
    deaths = main[1].get_attribute('innerHTML')
    recoveres = main[2].get_attribute('innerHTML')
   
    element = driver.find_element_by_id('main_table_countries_today')
    html_content = element.get_attribute('outerHTML')   

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    df_full = pd.read_html(str(table))[0]

    df = df_full.to_csv(index=False)

    # print(df)
    f = open('covid_table.txt', 'w+')
    f.write(df)

    # IMPORTANT

    # estruturar conteudo em data fame - PANDAS
    # df_full = pd.read_html(str(table))[0]
    # df = df_full[['Country,Other', 'TotalCases']]
    # df.columns = ['Pais', 'Total de Casos']
    # print(df_full)

    # f = open('covid_table.txt', 'w+')
    # f.write(df_full.to_string())

    # IMPORTANT

    driver.quit()


    # SAMPLE:
    # CONTEUDO ATUALIZADO SOBRE O COVID-19

    # Data: 30/03/2020
    # Horario: 01:00

    # CASOS NO BRASIL: 
    # MORTES NO BRASIL:
    # RECUPERADOS:

    # CASOS NO MUNDO: 722,196
    # MORTES: 33,976
    # RECUPERADOS: 151,766

    

    date = formatDate(str(datetime.now()))

    post = ('CONTEUDO ATUALIZADO SOBRE O COVID-19\n\n' +
                        date + '\n\n' +
                        'CASOS NO MUNDO: ' + cases + '\n' +
                        'MORTES: ' + deaths + '\n' +
                        'RECUPERADOS: ' + recoveres + '\n')

    # tweets string
    # api.update_status(post)

    # print (post)


    time.sleep(15)




