
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
import csv
import random

#credentials to login to twitter api
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

# login to twitter account api
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)

# date to Brazilian format
def formatDate(hour):
    day = hour[8:10]
    mon = hour[5:7]
    year = hour[:4]
    full_date = day + '/' + mon + '/' + year
    
    hours = hour[11:16]

    full_string = ('Data: ' + full_date + '\n' + 
                    'Horario: ' + hours)

    return full_string


# infinite loop to keep posting tweets
while (True):    
    # web page to get data from
    url = 'https://www.worldometers.info/coronavirus/'

    option = Options()
    option.headless = True
    
    # firefox to load web page, if 'options=option' deleted ...
    # ... browser opens and you can see the process going on
    driver = webdriver.Firefox(options=option)
    driver.get(url)

    time.sleep(10) # wait until web page is fully loaded

    # get main element with worldwide info (cases, deaths and recovered)
    main = driver.find_elements_by_xpath("//div[@class='maincounter-number']//span")

    cases = main[0].get_attribute('innerHTML')
    deaths = main[1].get_attribute('innerHTML')
    recoveres = main[2].get_attribute('innerHTML')
   
    # get main content table with worldwide info
    element = driver.find_element_by_id('main_table_countries_today')
    html_content = element.get_attribute('outerHTML')   

    # beautifulsoup to parse html and get table element
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # pandas reads full html table and converts to csv
    df_full = pd.read_html(str(table))[0]
    df = df_full.to_csv(index=False)

    f = open('covid_tb2.csv', 'w+')
    f.write(df)

    brazil = ''

    # opens csv, iterates through the file in search of Brazil ...
    # ... and builds string to tweet
    file2 = csv.reader(open('covid_tb2.csv'), delimiter=',')
    x = 0
    flag = False
    for line in file2:
        for i in range(len(line)):
            if (line[i] == 'Brazil'):
                brazil = ('CASOS NO BRASIL: ' + line[1] + '\n' +
                            'MORTES: ' + line[3] + '\n' +
                            'CURADOS: ' + line[5] + '\n\n')
                flag = True
                break
        if (flag):
                break
        
    driver.quit()    

    date = formatDate(str(datetime.now()))

    # concat final string to be posted
    post = ('CONTEUDO ATUALIZADO SOBRE O COVID-19\n\n' +
                        date + '\n\n' +
                        brazil +
                        'CASOS NO MUNDO: ' + cases + '\n' +
                        'MORTES: ' + deaths + '\n' +
                        'CURADOS: ' + recoveres)

    # tweets string
    api.update_status(post)

    # generates random number in range (120, 300) representing seconds
    # tweets have an interval of 2 to 3 minutes
    t = random.randrange(120, 300)

    # sleep the random generate seconds until next post
    time.sleep(t)




