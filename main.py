# -*- coding: utf-8 -*-
from datetime import datetime
import locale
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')



headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}


# cria uma lista para receber dados
dic_noti = []
for i in range(1, 500):

    url_pag = f'https://www.bbc.com/portuguese/topics/cz74k717pw5t?page={i}'
    r = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    noticia = soup.find_all('li', attrs={'class': 'bbc-1hw65ki e19ndkkm1'})
    # Percorre todas noticias da pagina estipulada
    for a in noticia:
        titulo = a.find('a', class_=re.compile('bbc-uk8dsi e1d658bg0'))
        data_pub = a.find('time', class_='bbc-16jlylf e1mklfmt0')
        url2 = titulo['href']
        link2 = [url2]
        data1 = data_pub.text
        #data = datetime.strptime(data1, "%d %B %Y") #função ainda n implementada.
        for w in link2:
            r2 = requests.get(url2, headers=headers)
            soup2 = BeautifulSoup(r2.content, 'html.parser')
            resumo = soup2.find('p', attrs={'class': 'bbc-hhl7in e17g058b0'})
        
        if (resumo):
            dic_noti.append([titulo.text, resumo.text, titulo['href'], data1])
        else:
            dic_noti.append([titulo.text, '', titulo['href'], data1])
    print('next')
# cria tabela de dados para receber as informações
df = pd.DataFrame(dic_noti, columns=['Título','Resumo','Link', 'Data'])

df.to_excel('rapagem_CNN3.xls')